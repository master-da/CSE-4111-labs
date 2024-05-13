from CTK import CTK
import random
import math

EXPLORATION_CONSTANT = 2
GAME_SIZE = 6

class Node:
    parent: 'Node' = None
    children: list['Node'] = None
    move: tuple[int, int] = None
    maximizingPlayer = None
    visits = 0
    t = 0

    def __init__(self, maximizingPlayer: bool, parent: 'Node', move: tuple[int, int]):
        self.maximizingPlayer = maximizingPlayer
        self.parent = parent
        self.move = move
        self.children = []
    
    def ucb1(self):
        if self.visits == 0: return math.inf
        return self.t + EXPLORATION_CONSTANT * math.log(self.parent.visits / self.visits)
    
    def rollout(self, game: CTK):
        turn = self.maximizingPlayer
        
        while not game.ifEndGame():
            
            player = game.max_player_state if turn is True else game.min_player_state
            
            moveset = []
            for piece in range(game.size+1):
                if player[piece] is not None:
                    moveset += [(piece, move) for move in game.getLegalMoveSet(turn, piece)]
            
            if (len(moveset) == 0): return 0
            
            piece, move = random.choice(moveset)
            game.makeMove(turn, piece, move)
            # print((piece, move))
            # print(game)
            
            turn = not turn
        if game.max_player_state[0] is None:
            return -1
        return 1
    
    def expand(self, game: CTK):
        player = game.max_player_state if self.maximizingPlayer else game.min_player_state
        for piece in range(game.size+1):
            if player[piece] is not None:
                for move in game.getLegalMoveSet(self.maximizingPlayer, piece):
                    self.children.append(Node(not self.maximizingPlayer, self, (piece, move)))
                    
    def backpropagate(self, result):
        self.visits += 1
        self.t += result
        if self.parent is not None:
            self.parent.backpropagate(result)
            
    
            
if __name__ == "__main__":
    game = CTK(GAME_SIZE)
    root = Node(True, None, None)
    root.expand(game)
    
    # for i in range(1000):
    while True:
        game = CTK(GAME_SIZE)
        node = root
        while len(node.children) > 0:
            
            # max_child = max(node.children, key=lambda x: x.ucb1())
            # piece, move = max_child.move
            # game.makeMove(node.maximizingPlayer, piece, move)
            # node = max_child

            child: Node = None
            if node.maximizingPlayer: child = max(node.children, key=lambda x: x.ucb1())
            else: child = min(node.children, key=lambda x: x.ucb1())
            piece, move = child.move
            game.makeMove(node.maximizingPlayer, piece, move)
            node = child
            

        if game.ifEndGame():
            break

        if node.visits != 0:
            node.expand(game)
            if len(node.children) > 0: node = node.children[0]
            else: continue
            

        result = node.rollout(game)
        node.backpropagate(result)
        
    game = CTK(GAME_SIZE)
    node = root
    print(game)
    while len(node.children) > 0:
        
        child: Node = None
        if node.maximizingPlayer: child = max(node.children, key=lambda x: x.ucb1())
        else: child = min(node.children, key=lambda x: x.ucb1())
        
        piece, move = child.move

        print(game.max_player_state, game.min_player_state)
        
        game.makeMove(node.maximizingPlayer, piece, move)

        print("Player 1" if node.maximizingPlayer else "Player 2", (piece, move))
        print(game)
        
        node = child
    