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

        self.l1 = nn.Linear(state_dim, hidden_dim)
        self.l2 = nn.Linear(hidden_dim, hidden_dim)
        self.l3 = nn.Linear(hidden_dim, 1)

    def forward(self, state):
        v = torch.relu(self.l1(state))
        v = torch.relu(self.l2(v))
        v = self.l3(v)
        return v


class SAC():
    def __init__(self, state_dim, action_dim, hidden_dim=200, gamma=0.99, 
                                                lmbda=0.95, lr=1e-4, 
                                                clip_rate=0.2, 
                                                batch_size=64,
                                                entropy_coef_decay=0.99,
                                                entropy_coef = 1e-3,
                                                n_epochs=10,
                                                weight_decay=1e-3, alpha=0.1):


        self.actor = Actor(state_dim, action_dim, hidden_dim).to(device)
        self.critic_1 = Critic(state_dim, hidden_dim).to(device)
        self.critic_2 = Critic(state_dim, hidden_dim).to(device)

        self.critic_target_1 = Critic(state_dim, hidden_dim).to(device)
        self.critic_target_2 = Critic(state_dim, hidden_dim).to(device)

        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), lr=lr, weight_decay=weight_decay)
        self.critic_optimizer_1 = torch.optim.Adam(self.critic_1.parameters(), lr=lr, weight_decay=weight_decay)
        self.critic_optimizer_2 = torch.optim.Adam(self.critic_2.parameters(), lr=lr, weight_decay=weight_decay)
        
        self.critic_target_optimizer_1 = torch.optim.Adam(self.critic_target_1.parameters(), lr=lr, weight_decay=weight_decay)
        self.critic_target_optimizer_2 = torch.optim.Adam(self.critic_target_2.parameters(), lr=lr, weight_decay=weight_decay)

        self.state_dim = state_dim
        self.data = []
        self.alpha = alpha
        self.gamma = gamma
        self.lmbda = lmbda
        self.clip_rate = clip_rate
        self.n_epochs = n_epochs
        self.optim_batch_size = batch_size

        self.entropy_coef = entropy_coef
        self.entropy_coef_decay = entropy_coef_decay

    def select_action(self, state, evaluate=False):
        # Deterministic policy
        if evaluate:
            with torch.no_grad():
                pi = self.actor.pi(state, softmax_dim=0)
                a = torch.argmax(pi).item()
            return a, 1.0

        # Stochastic policy
        with torch.no_grad():
            pi = self.actor.pi(state, softmax_dim=0)
            m = Categorical(pi)
            a = m.sample().item()
            pi_a = pi[a].item()
        return a, pi_a

    def soft_update(self, tau=0.1):
        for target_param, local_param in zip(self.critic_target_1.parameters(), self.critic_1.parameters()):
            target_param.data.copy_(tau * local_param.data + (1 - tau) * target_param.data)

        for target_param, local_param in zip(self.critic_target_2.parameters(), self.critic_2.parameters()):
            target_param.data.copy_(tau * local_param.data + (1 - tau) * target_param.data)

    def train(self):
        s, a, r, s_prime, old_prob_a,done= self.make_batch()
        self.entropy_coef *= self.entropy_coef_decay #exploring decay
        self.soft_update(tau=1.0)
        with torch.no_grad():
            vs_1 = self.critic_1(s)
            vs_prime_1 = self.critic_target_1(s_prime)

            deltas_1 = r + self.gamma * vs_prime_1  - vs_1
            deltas_1 = deltas_1.cpu().flatten().numpy()
            adv_1 = [0]

            for delta in deltas_1[::-1]:
                advantage = delta + self.gamma * self.lmbda * adv_1[-1] 
                adv_1.append(advantage)
            adv_1.reverse()
            adv_1 = copy.deepcopy(adv_1[0:-1])
            adv_1 = torch.tensor(adv_1).unsqueeze(1).float().to(device)
            td_target_1 = adv_1 + vs_1
            adv_1 = (adv_1 - adv_1.mean()) / ((adv_1.std() + 1e-4))  

            vs_2 = self.critic_2(s)
            vs_prime_2 = self.critic_target_2(s_prime)

            deltas_2 = r + self.gamma * vs_prime_2  - vs_2
            deltas_2 = deltas_2.cpu().flatten().numpy()
            adv_2 = [0]

            for delta in deltas_2[::-1]:
                advantage = delta + self.gamma * self.lmbda * adv_2[-1] 
                adv_2.append(advantage)
            adv_2.reverse()
            adv_2 = copy.deepcopy(adv_2[0:-1])
            adv_2 = torch.tensor(adv_2).unsqueeze(1).float().to(device)
            td_target_2 = adv_2 + vs_2
            adv_2 = (adv_2 - adv_2.mean()) / ((adv_2.std() + 1e-4))  

        optim_iter_num = int(math.ceil(s.shape[0] / self.optim_batch_size))
        for _ in range(self.n_epochs):
            perm = np.arange(s.shape[0])
            np.random.shuffle(perm)
            perm = torch.LongTensor(perm).to(device)
            s, a, td_target_1, adv_1, td_target_2, adv_2, old_prob_a = \
                s[perm].clone(), a[perm].clone(), td_target_1[perm].clone(), adv_1[perm].clone(), td_target_2[perm].clone(), adv_2[perm].clone(), old_prob_a[perm].clone()


            # PPO update
            for i in range(optim_iter_num):
                index = slice(i * self.optim_batch_size, min((i + 1) * self.optim_batch_size, s.shape[0]))

                # Update the actor
                prob = self.actor.pi(s[index], softmax_dim=1)
                entropy = Categorical(prob).entropy().sum(0, keepdim=True)
                prob_a = prob.gather(1, a[index])
                
                q_values_1 = self.critic_1(s[index])
                q_values_2 = self.critic_2(s[index])

                inside_term = self.alpha*torch.log(prob_a) - torch.min(q_values_1, q_values_2)
                a_loss = (prob_a*inside_term).sum(dim=1).mean()

                self.actor_optimizer.zero_grad()
                a_loss.backward()
                torch.nn.utils.clip_grad_norm_(self.actor.parameters(), 40)
                self.actor_optimizer.step()

                # Update the critic
                c_1_loss = (self.critic_1(s[index]) - td_target_1[index]).pow(2).mean()
                c_2_loss = (self.critic_2(s[index]) - td_target_2[index]).pow(2).mean()

                self.critic_optimizer_1.zero_grad()
                c_1_loss.backward()
                self.critic_optimizer_1.step()

                self.critic_optimizer_2.zero_grad()
                c_2_loss.backward()
                self.critic_optimizer_2.step()

                self.soft_update()

        return a_loss.mean(), c_1_loss+c_2_loss, entropy

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

