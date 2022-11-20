import gym 
import numpy as np


if __name__ == '__main__':
    n_steps = 2000
    n_episodes = 100 
    env = gym.make("gym_ants:ants-v0")
    state = env.reset()
    for e in range(n_episodes):
        state = env.reset()
        for s in range(n_steps):
            actions = np.random.randint(3, size=10)
            env.step(actions)
            env.render()
    env.close()