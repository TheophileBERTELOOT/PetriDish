import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from torch.distributions import Categorical
import copy
import math


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Actor(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim):
        super(Actor, self).__init__()

        self.l1 = nn.Linear(state_dim, hidden_dim)
        self.l2 = nn.Linear(hidden_dim, hidden_dim)
        self.l3 = nn.Linear(hidden_dim, action_dim)


    def forward(self, state):
        n = torch.tanh(self.l1(state))
        n = torch.tanh(self.l2(n))
        return n

    def pi(self, state, softmax_dim = 0):
        n = self.forward(state)
        prob = F.softmax(self.l3(n), dim=softmax_dim)
        return prob


class Critic(nn.Module):
    def __init__(self, state_dim,hidden_dim):
        super(Critic, self).__init__()

        self.C1 = nn.Linear(state_dim, hidden_dim)
        self.C2 = nn.Linear(hidden_dim, hidden_dim)
        self.C3 = nn.Linear(hidden_dim, 1)

    def forward(self, state):
        v = torch.relu(self.C1(state))
        v = torch.relu(self.C2(v))
        v = self.C3(v)
        return v


class PPO():
    def __init__(self, state_dim, action_dim, hidden_dim=200, gamma=0.99, 
                                                lmbda=0.95, lr=1e-4, 
                                                clip_rate=0.2, 
                                                batch_size=64,
                                                entropy_coef_decay=0.99,
                                                entropy_coef = 1e-3,
                                                n_epochs=10,
                                                weight_decay=1e-3):


        self.actor = Actor(state_dim, action_dim, hidden_dim).to(device)
        self.critic = Critic(state_dim, hidden_dim).to(device)

        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), lr=lr, weight_decay=weight_decay)
        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), lr=lr, weight_decay=weight_decay)
        
        self.state_dim = state_dim
        self.data = []
        self.gamma = gamma
        self.lmbda = lmbda
        self.clip_rate = clip_rate
        self.n_epochs = n_epochs
        self.optim_batch_size = batch_size

        self.entropy_coef = entropy_coef
        self.entropy_coef_decay = entropy_coef_decay

    def select_action(self, state):
        '''Stochastic Policy'''
        with torch.no_grad():
            pi = self.actor.pi(state, softmax_dim=0)
            m = Categorical(pi)
            a = m.sample().item()
            pi_a = pi[a].item()
        return a, pi_a

    def evaluate(self, state):
        '''Deterministic Policy'''
        with torch.no_grad():
            pi = self.actor.pi(state, softmax_dim=0)
            a = torch.argmax(pi).item()
        return a,1.0


    def train(self):
        s, a, r, s_prime, old_prob_a,done= self.make_batch()
        self.entropy_coef *= self.entropy_coef_decay #exploring decay

        with torch.no_grad():
            vs = self.critic(s)
            vs_prime = self.critic(s_prime)

            deltas = r + self.gamma * vs_prime  - vs
            deltas = deltas.cpu().flatten().numpy()
            adv = [0]

            for delta in deltas[::-1]:
                advantage = delta + self.gamma * self.lmbda * adv[-1] 
                adv.append(advantage)
            adv.reverse()
            adv = copy.deepcopy(adv[0:-1])
            adv = torch.tensor(adv).unsqueeze(1).float().to(device)
            td_target = adv + vs
            adv = (adv - adv.mean()) / ((adv.std() + 1e-4))  


        optim_iter_num = int(math.ceil(s.shape[0] / self.optim_batch_size))

        for _ in range(self.n_epochs):
            perm = np.arange(s.shape[0])
            np.random.shuffle(perm)
            perm = torch.LongTensor(perm).to(device)
            s, a, td_target, adv, old_prob_a = \
                s[perm].clone(), a[perm].clone(), td_target[perm].clone(), adv[perm].clone(), old_prob_a[perm].clone()

            '''mini-batch PPO update'''
            for i in range(optim_iter_num):
                index = slice(i * self.optim_batch_size, min((i + 1) * self.optim_batch_size, s.shape[0]))

                '''actor update'''
                prob = self.actor.pi(s[index], softmax_dim=1)
                entropy = Categorical(prob).entropy().sum(0, keepdim=True)
                prob_a = prob.gather(1, a[index])
                ratio = torch.exp(torch.log(prob_a) - torch.log(old_prob_a[index]))  # a/b == exp(log(a)-log(b))

                surr1 = ratio * adv[index]
                surr2 = torch.clamp(ratio, 1 - self.clip_rate, 1 + self.clip_rate) * adv[index]
                a_loss = -torch.min(surr1, surr2) - self.entropy_coef * entropy

                self.actor_optimizer.zero_grad()
                a_loss.mean().backward()
                torch.nn.utils.clip_grad_norm_(self.actor.parameters(), 40)
                self.actor_optimizer.step()

                '''critic update'''
                c_loss = (self.critic(s[index]) - td_target[index]).pow(2).mean()

                self.critic_optimizer.zero_grad()
                c_loss.backward()
                self.critic_optimizer.step()
        return a_loss.mean(), c_loss, entropy

    def make_batch(self):
        l = len(self.data)
        s_lst, a_lst, r_lst, s_prime_lst, prob_a_lst, done_lst= \
            np.zeros((l,self.state_dim)), np.zeros((l,1)), np.zeros((l,1)), np.zeros((l,self.state_dim)), np.zeros((l,1)), np.zeros((l,1))
            
        for i,transition in enumerate(self.data):
            s_lst[i], a_lst[i],r_lst[i] ,s_prime_lst[i] ,prob_a_lst[i] ,done_lst[i]  = transition
        

        self.data = [] #Clean history trajectory

        '''list to tensor'''
        with torch.no_grad():
            s,a,r,s_prime,prob_a,done = \
                torch.tensor(s_lst, dtype=torch.float).to(device), \
                torch.tensor(a_lst, dtype=torch.int64).to(device), \
                torch.tensor(r_lst, dtype=torch.float).to(device), \
                torch.tensor(s_prime_lst, dtype=torch.float).to(device), \
                torch.tensor(prob_a_lst, dtype=torch.float).to(device), \
                torch.tensor(done_lst, dtype=torch.float).to(device), \

        return s, a, r, s_prime, prob_a,done

    def put_data(self, transition):
        self.data.append(transition)

    def save(self, episode):
        torch.save(self.critic.state_dict(), "./model/ppo_critic{}.pth".format(episode))
        torch.save(self.actor.state_dict(), "./model/ppo_actor{}.pth".format(episode))

    def load(self, episode):
        self.critic.load_state_dict(torch.load("./model/ppo_critic{}.pth".format(episode)))
        self.actor.load_state_dict(torch.load("./model/ppo_actor{}.pth".format(episode)))

