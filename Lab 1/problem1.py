import osmnx as ox
import matplotlib.pyplot as plt
import pickle
from queue import PriorityQueue
import time

place = "New York City, New York, USA"

# # get the network for the city of interest
# G = ox.graph_from_place(place)

# with open('cache.pkl', 'wb') as f:
#     pickle.dump(G, f)

G = None
with open('cache.pkl', 'rb') as f:
    G = pickle.load(f)

start = list(G.nodes())[0]
end = list(G.nodes())[20]

def _heuristic(graph, node, dest):
    neighbors = list(graph.neighbors(node))
    risk = 1/max(len(neighbors), 1) 
    h_sld = ox.distance.euclidean(graph.nodes[node]['y'], graph.nodes[node]['x'], graph.nodes[dest]['y'], graph.nodes[dest]['x'])
    return h_sld + risk    

# # implement best first search to find a path between start and end nodes
def best_first_search(graph, start, end):

    path = {start: [start]}
    search_space = [start]
    vis = {}

    pq = PriorityQueue()
    pq.put((_heuristic(graph, start, end), start))
    vis[start] = True
    
    while not pq.empty():
        current = pq.get()
        vis[current[1]] = True
        search_space.append(current[1])
        if current[1] == end:
            break
        for next in graph.neighbors(current[1]):
            if next not in vis:
                path[next] = path[current[1]] + [next]
                pq.put((_heuristic(graph, next, end), next))
          
    return path[end], search_space

# implement the heuristic function for the weighted A* search. it needs to be admissible and consistent
def _a_star_heuristic(graph, node, dest, weight = 1):
    # get the shortest distance from start to node
    
    current_cost = ox.distance.euclidean(graph.nodes[start]['y'], graph.nodes[start]['x'], graph.nodes[node]['y'], graph.nodes[node]['x'])
    heuristic_cost = _heuristic(graph, node, dest)
    
    return current_cost + weight * heuristic_cost

# implement the weighted A* search to find a path between start and end nodes
def a_star_search_weighted(graph, start, end, weight):
    path = {start: [start]}
    vis = {}
    search_space = [start]
    look = {}
    pq = PriorityQueue()
    pq.put((_a_star_heuristic(graph, start, end, weight), start))
    vis[start] = True
    look[start] = True
    
    while not pq.empty():
        current = pq.get()
        vis[current[1]] = True
        look[current[1]] = True
        search_space.append(current[1])
        if current[1] == end:
            break
        for next in graph.neighbors(current[1]):
            if next not in look :
                path[next] = path[current[1]] + [next]
                look[next] = True
                pq.put((_a_star_heuristic(graph, next, end, weight), next))
            
    return path[end], search_space

if __name__ == "__main__":

    bfs_start_time = time.time()
    bfs_path, bfs_explore = best_first_search(G, start, end)
    bfs_time = time.time() - bfs_start_time

    a_star_start_time = time.time()
    a_star_path, a_star_explore = a_star_search_weighted(G, start, end, 1)
    a_star_time = time.time() - a_star_start_time

    a_star_weighted_start_time = time.time()
    a_star_path_weighted_path, a_star_path_weighted_explore = a_star_search_weighted(G, start, end, 4)
    a_star_weighted_time = time.time() - a_star_weighted_start_time
    
    it_time = []
    for i in range(10):
        t = time.time()
        _, _ = a_star_search_weighted(G, start, end, i+1)
        it_time.append(time.time() - t)        

    # plot the time taken in a bar chart
    fig, ax = plt.subplots()
    ax.bar(['Best First Search', 'A* Search'] + [f"W - {i+1}" for i in range(len(it_time))] , [bfs_time, a_star_time]+ it_time)
    ax.set_ylabel('Time (s)')
    ax.set_title('Time taken by each algorithm')
    plt.show()

    fig, ax = ox.plot_graph_routes(G, [bfs_path, a_star_path, a_star_path_weighted_path], route_colors=['blue', 'red', 'green'], route_linewidth=2, show=False, close=False)
    plt.show()

    # scatter the explore points on a graph for each of the three algorithms
    fig, ax = ox.plot_graph(G, show=False, close=False)
    ax.scatter([G.nodes[i]['x'] for i in a_star_explore], [G.nodes[i]['y'] for i in a_star_explore], c='red', s=12)
    ax.scatter([G.nodes[i]['x'] for i in a_star_path_weighted_explore], [G.nodes[i]['y'] for i in a_star_path_weighted_explore], c='green', s=24)
    ax.scatter([G.nodes[i]['x'] for i in bfs_explore], [G.nodes[i]['y'] for i in bfs_explore], c='blue', s=4)
    ax.scatter(G.nodes[start]['x'], G.nodes[start]['y'], c='black', s=30)
    plt.show()
