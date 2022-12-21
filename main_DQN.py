from poutyne import Model
from copy import deepcopy  # NEW

import numpy as np
import gym
import torch
import random
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot


class ReplayBuffer:
    def __init__(self, buffer_size):
        self.__buffer_size = buffer_size
        self.data = []
        

    def store(self, element):
        '''
        Stores an element. If the replay buffer is already full, deletes the oldest
        element to make space.
        '''
        
        # TODO: implement
        self.data.append(element)

        if (len(self.data) > self.__buffer_size) : 
            del self.data[0]

        

    def get_batch(self, batch_size):
        '''
        Returns a list of batch_size elements from the buffer.
        '''
        
        # TODO: implement
        return random.choices(self.data, k=batch_size)


def evaluate_policy(env, model, render):
    scores = 0
    turns = 1
    for j in range(turns):
        states, done, ep_rewards, steps = env.reset(), False, 0, 0
        steps = 0
        ep_r = 0
        while not done and steps < 600:
            actions = []
            for s in states:
                q_vals =model.predict_on_batch(s.astype(np.float32)) 
                actions.append(model.select_action(q_vals, epsilon=0, evaluate=True))
            next_states, rewards, done, info = env.step(actions)
            ep_r += np.sum(rewards)
            steps += 1
            states = next_states
            if render:
                env.render()
        scores += ep_r
    return scores/turns

class DQN(Model):
    def __init__(self, actions, *args, **kwargs):
        self.actions = actions
        super().__init__(*args, **kwargs)

    def select_action(self, state, epsilon=0, evaluate=False):
        '''
        Returns the selected action according to an epsilon-greedy policy.
        '''

        if np.random.rand() < epsilon and not evaluate:
            action = self.actions.sample()
        else:
            action =  np.argmax(state)
        
        return action

    def soft_update(self, other, tau):
        '''
        Code for the soft update between a target network (self) and
        a source network (other).

        The weights are updated according to the rule in the assignment.
        '''
        new_weights = {}

        own_weights = self.get_weight_copies()
        other_weights = other.get_weight_copies()

        for k in own_weights:
            new_weights[k] = (1 - tau) * own_weights[k] + tau * other_weights[k]

        self.set_weights(new_weights)


class NNModel(torch.nn.Module):
    '''
    Neural Network with 3 hidden layers of hidden dimension 64.
    '''

    def __init__(self, in_dim, out_dim, n_hidden_layers=3, hidden_dim=64):
        super().__init__()
        layers = [torch.nn.Linear(in_dim, hidden_dim), torch.nn.ReLU()]
        for _ in range(n_hidden_layers - 1):
            layers.extend([torch.nn.Linear(hidden_dim, hidden_dim), torch.nn.ReLU()])
        layers.append(torch.nn.Linear(hidden_dim, out_dim))

        self.fa = torch.nn.Sequential(*layers)

    def forward(self, x):
        return self.fa(x)


def format_batch(batch, target_network, gamma):
    '''
    Input : 
        - batch, a list of n=batch_size elements from the replay buffer
        - target_network, the target network to compute the one-step lookahead target
        - gamma, the discount factor

    Returns :
        - states, a numpy array of size (batch_size, state_dim) containing the states in the batch
        - (actions, targets) : where actions and targets both
                      have the shape (batch_size, ). Actions are the 
                      selected actions according to the target network
                      and targets are the one-step lookahead targets.
    '''
    
    states = np.array([x[0] for x in batch])    
    actions = np.array([x[1] for x in batch])
    rewards = np.array([x[2] for x in batch])  
    next_states = np.array([x[3] for x in batch])  
    dones = np.array([x[4] for x in batch])

    next_q_vals = target_network.predict_on_batch(next_states)

    max_qvals = np.max(next_q_vals, axis=-1)
    targets = rewards + gamma * max_qvals * (1 -dones)
    targets = targets.astype(np.float32)
    return states, (actions, targets)


def dqn_loss(y_pred, y_target):
    '''
    Input :
        - y_pred, (batch_size, n_actions) Tensor outputted by the network
        - y_target = (actions, targets), where actions and targets both
                      have the shape (batch_size, ). Actions are the 
                      selected actions according to the target network
                      and targets are the one-step lookahead targets.

    Returns :
        - The DQN loss 
    '''
    

    actions, Q_target = y_target
    
    try:
        Q_predict = y_pred.gather(1, actions.unsqueeze(-1).to(torch.int64)).squeeze()
    except:
        print(actions, y_pred.shape)
    return torch.nn.functional.mse_loss(Q_predict, Q_target)


def set_random_seed(environment, seed):
    environment.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)  # NEW


def run(batch_size, gamma, buffer_size, seed, tau, training_interval, learning_rate):
    environment = gym.make('gym_ants:ants-v0')
    eval_env = gym.make('gym_ants:ants-v0')
    eval_env.seed(seed)
    set_random_seed(environment, seed)


    model = NNModel(6, 4)
    nb_trajectories = 500


    source_agent = DQN(environment.action_space, network=model, optimizer=torch.optim.Adam(model.parameters(), lr=learning_rate), loss_function=dqn_loss)
    target_agent = DQN(environment.action_space, network=model, optimizer=torch.optim.Adam(model.parameters(), lr=learning_rate), loss_function=dqn_loss)

    replay_buffer = ReplayBuffer(buffer_size)
    epsilon = 1.0
    R_trajectories = np.zeros(nb_trajectories)
    loss = []
    avg_training_loss = np.zeros(nb_trajectories)

    for n_trajectories in range(nb_trajectories):
        trajectory_done = False

        G = 0

        states = environment.reset()
        step_count = 1
        mean_loss = []
        while not trajectory_done and step_count <600:
            #environment.render()
            actions = []
            for s in states:
                q_vals =target_agent.predict_on_batch(s.astype(np.float32)) 
                actions.append(target_agent.select_action(q_vals, epsilon))
            next_states, rewards, trajectory_done, _ = environment.step(actions)
            G += np.sum(rewards)
            for (s, a, r, next_s) in zip(states, actions, rewards, next_states):
                replay_buffer.store((s.astype(np.float32)  , a, r, next_s.astype(np.float32)  , trajectory_done))

            if len(replay_buffer.data) > batch_size :
                if (step_count % training_interval == 0) :
                    minibatch = replay_buffer.get_batch(batch_size)
                    
                    states_, (actions_taken, targets) = format_batch(minibatch, target_agent, gamma)
                    loss_ = source_agent.train_on_batch(states_, (actions_taken, targets))
                    loss.append(loss_)
                    mean_loss.append(loss_)
                    target_agent.soft_update( source_agent, tau)

            states = next_states
            step_count += 1
            
        if n_trajectories % 10 == 0:

            loss_mean = loss[-1]
            score = evaluate_policy(eval_env, target_agent, render=False)
            print('Epoch {}:'.format(n_trajectories),'score:', score)
            #print(f"After {n_trajectories} trajectories, we have G_0 = {G:.2f}, loss {loss_mean}, epsilon  {epsilon:4f}")
        

        epsilon = max(0.99*epsilon, 0.01)
        R_trajectories[n_trajectories] = G
        avg_training_loss[n_trajectories] = np.mean(np.array(mean_loss))

    done = False
    s = environment.reset().astype(np.float32)
    environment.close()
    # while not done:
    #     environment.render()
    #
    #     q_vals = target_agent.predict_on_batch(s)
    #     action = np.argmax(q_vals)
    #     next_s, r, done, _ = environment.step(action)
    #     s = next_s
    # environment.close()

    fig, subfigs = pyplot.subplots(2, 1, tight_layout=True)
    labels = ["cumulative reward", "Average training loss"]
    x_labels = ['episodes','episodes']
    fig_to_plot = [R_trajectories, avg_training_loss]
    for subfig, index in zip(subfigs.reshape(-1), range(2)):
        subfig.plot(fig_to_plot[index], label=labels[index])
        subfig.set_xlabel(x_labels[index])
        subfig.legend()
    pyplot.savefig('test_enemy_3_randomFood.png')
    

if __name__ == "__main__":
    '''
    All hyperparameter values and overall code structure are only given as a baseline. 
    
    You can use them if they help  you, but feel free to implement from scratch the
    required algorithms if you wish!
    '''
    batch_size =64
    gamma = 0.9
    buffer_size = 4e5
    seed = 42
    tau = 0.1
    training_interval = 3
    learning_rate = 1*1e-4

    run(batch_size, gamma, buffer_size, seed, tau, training_interval, learning_rate)
