import gym 
import numpy as np


if __name__ == '__main__':
    env = gym.make("gym_ants:ants-v0")
    state = env.reset()
    print(state)
    actions = np.random.randint(3, size=10)
    print(env.step(actions))