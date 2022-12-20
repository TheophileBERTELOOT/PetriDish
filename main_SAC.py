import gym
import torch
import os, shutil
import numpy as np
from tqdm import tqdm
from rl_agents.SAC import device, SAC
import matplotlib.pyplot as plt
import pickle

def evaluate_policy(env, model, render):
    scores = 0
    turns = 1
    for j in range(turns):
        states, done, ep_rewards, steps = env.reset(), False, 0, 0
        steps = 0
        ep_r = 0
        while not done and steps < 600:
            actions, pi_actions = [], []
            for s in states:
                a, pi_a = model.select_action(torch.from_numpy(s).float().to(device), evaluate=True)
                actions.append(a)
                pi_actions.append(pi_a)
            next_states, rewards, done, info = env.step(actions)
            ep_r += np.sum(rewards)
            steps += 1
            states = next_states
            if render:
                env.render()
        scores += ep_r
    return scores/turns


def main():
    env = gym.make('gym_ants:ants-v0')
    eval_env = gym.make('gym_ants:ants-v0')

    seed = 42
    torch.manual_seed(seed)
    env.seed(seed)
    eval_env.seed(seed)
    np.random.seed(seed)

    load_model = False

    state_dim = 3
    action_dim = 4
    hidden_dim = 200
    gamma = 0.99
    lmbda=0.95
    lr=1e-4
    clip_rate=0.2
    batch_size=64
    entropy_coef_decay=0.9
    entropy_coef = 1e-4
    n_epochs=10
    weight_decay=1e-3
    training_epochs = 1000

    eval_interval = 10 
    save_interval = 100 
    save_model = True
    ModelIdex = None # Index of the model to load

    if not os.path.exists('model'): os.mkdir('model')
    model = SAC(state_dim, action_dim, hidden_dim, gamma, lmbda, lr, clip_rate, 
                batch_size, entropy_coef_decay, entropy_coef, n_epochs, weight_decay)

    if load_model: 
        model.load(ModelIdex)


    total_steps = 0

    scores_history = []

    for epoch in tqdm(range(training_epochs)):
        states, done, steps, ep_r = env.reset(), False, 0, 0

        #Training the model
        steps = 0
        while  steps < 600:
            steps += 1
            actions, pi_actions =[], []
            for s in states:
                a, pi_a = model.select_action(torch.from_numpy(s).float().to(device))
                actions.append(a)
                pi_actions.append(pi_a)

            actions = np.array(actions)
            pi_actions = np.array(pi_actions)
            next_states, rewards, done, info = env.step(actions)
            # env.render()

            
            for s, s_prime, a, r in zip(states, next_states, actions, rewards):
                model.put_data((s, a, r, s_prime, pi_a, done))
                ep_r += r
            states = next_states

        
        # print("a_loss : ", a_loss)
        # print("c_loss : ", c_loss)
        # print("entropy : ", entropy)


        if epoch % 10 == 0:
            a_loss, c_loss, entropy = model.train()
            # print("Actor loss : ", a_loss)
            # print("Critic loss : ", c_loss)

            score = evaluate_policy(eval_env, model, render=True)
            print('Epoch {}:'.format(epoch),'score:', score)
            scores_history.append(score)
            total_steps += 1

        """if save_model and epoch % save_interval==0:
            model.save(total_steps)"""

    with open('scores_history_SAC', 'wb') as fp:
        pickle.dump(scores_history, fp)


    plt.plot(scores_history)
    plt.xlabel("Épisodes")
    plt.ylabel("Récompense cumulative")
    plt.show()

    env.close()
    eval_env.close()

if __name__ == '__main__':
    main()
