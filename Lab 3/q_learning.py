import gymnasium
import numpy as np
import matplotlib.pyplot as plt

env = gymnasium.make("FrozenLake-v1")

Q = np.zeros([env.observation_space.n, env.action_space.n])

lr = .8
y = .95
eps = 0.1
num_episodes = 2000

rList = []

for i in range(num_episodes):
    s, _ = env.reset()
    rAll = 0
    j = 0

    for _ in range(1000):

        a = None
        if np.random.rand(1) < eps:
            a = env.action_space.sample()
        else:
            if np.all(Q[s, :]) == Q[s, 0]:
                a = env.action_space.sample()
            else:
                a = np.argmax(Q[s, :])

        s1, r, terminated, truncated, _ = env.step(a)

        Q[s, a] = Q[s, a] + lr * (r + y * np.max(Q[s1, :]) - Q[s, a])
        rAll += r
        s = s1

        if terminated or truncated:
            break

    rList.append(rAll)

# fig, ax = plt.subplots()
# ax.plot(np.cumsum(rList))
# ax.set(xlabel='Episode', ylabel='Cumulative Reward', title='Q-Learning on FrozenLake-v1')
# ax.grid()
# plt.show()

print("Score over time: " + str(sum(rList) / num_episodes))
print("Final Q-Table Values")
# print(Q)

# env = gymnasium.make("FrozenLake-v1", render_mode="human")
iterations = 1000
success_percent = np.zeros(iterations)
avg_steps = [[]] * iterations

for iter in range(iterations):
    for _ in range(20):
        s, _ = env.reset()
        steps = 0
        while True:
            a = np.argmax(Q[s, :])
            s, r, terminated, truncated, _ = env.step(a)
            steps += 1
            if terminated or truncated:
                if s == env.observation_space.n - 1:
                    success_percent[iter] += 1
                    avg_steps[iter].append(steps)
                break
    avg_steps[iter] = np.mean(avg_steps[iter])
print(np.mean(success_percent))
print(np.mean(avg_steps))