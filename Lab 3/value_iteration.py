import gymnasium
import numpy as np
import matplotlib.pyplot as plt

env = gymnasium.make("FrozenLake-v1")
lake = env.unwrapped.desc.flatten()

U = np.zeros(env.observation_space.n)
lr = 0.8
gamma = 0.95
eps = 0.0001
breaking_point = eps * (1 - gamma) / gamma

average_change = np.array([])

while True:
    U1 = np.zeros(env.observation_space.n)
    for s in range(env.observation_space.n):
        if lake[s] == b'H':
            U1[s] = 0
        else:
            U1[s] = np.max([gamma * np.sum([prob * U[next_state] for prob, next_state, _, _ in env.unwrapped.P[s][a]]) for a in range(env.action_space.n)])
            if lake[s] == b'G':
                U1[s] += 1

    if np.max(np.abs(U1 - U)) < breaking_point:
        break
    average_change = np.append(average_change, [np.mean(np.abs(U1 - U))])
    U = U1

policy = np.array([np.argmax([np.sum([prob * U[next_state] for prob, next_state, _, _ in env.unwrapped.P[s][a]]) for a in range(env.action_space.n)]) for s in range(env.observation_space.n)])

iterations = 1000
success_percent = np.zeros(iterations)
avg_steps = [[]] * iterations

for iter in range(iterations):
    for _ in range(20):
        steps = 0
        s, _ = env.reset()
        while True:
            a = policy[s]
            s, _, terminated, truncated, _ = env.step(a)
            steps += 1
            if terminated or truncated:
                if s == env.observation_space.n - 1:
                    success_percent[iter] += 1
                    avg_steps[iter].append(steps)
                    # print("Goal reached in " + str(steps) + " steps")
                break
    avg_steps[iter] = np.mean(avg_steps[iter])
print(success_percent)
print(avg_steps)
# fig, ax = plt.subplots()
# ax.plot(average_change)
# ax.set(xlabel='Iterations', ylabel='Average Change',
#        title='Value Iteration')
# ax.grid()
# plt.show()

env.close()