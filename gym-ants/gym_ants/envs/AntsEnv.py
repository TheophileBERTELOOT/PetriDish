import gym
from gym import spaces
import numpy as np
from gym_ants.config.AntsEnvConfig import *
from gym_ants.helpers.Display import Display
from gym_ants.helpers.MotionService import MotionService
from gym_ants.species.HerbivorCreator import HerbivorCreator
from gym_ants.species.CarnivoreCreator import CarnivoreCreator
from gym_ants.species.FourmieCreator import FourmieCreator
from gym_ants.helpers.Instance import Instance
from gym_ants.helpers.EventHandler import EventHandler
import pygame as pg

class AntsEnv(gym.Env):
	def __init__(self, render=True):
		self.action_space = spaces.Discrete(6)
		# self.observation_space = spaces.Box(low=0, high= 100000000, shape=(6))
		self.reward_range = (-200, 200)
		self.current_episode = 0
		self.success_episode = []
		self.fourmis = []
		self.rewards = [] 
		if render:
			pg.init()
			self.motionService = MotionService(SCREEN_SIZE_X,SCREEN_SIZE_Y)
			self.display = Display(SCREEN_SIZE_X,SCREEN_SIZE_Y, self.motionService)
			self.eventHandler = EventHandler(grassZoneEditRadius, self.motionService)

		self.herbivorCreator = HerbivorCreator(SCREEN_SIZE_X, SCREEN_SIZE_Y, nbHerbivore, herbivoreInitRadius,herbivoreInitHealth, herbivoreBonusHealthWhenEat, herbivoreReproductionThreshold, herbivoreHungrinessThreshold, herbivorePas)
		self.carnivorCreator = CarnivoreCreator(SCREEN_SIZE_X, SCREEN_SIZE_Y, nbCarnivore,carnivoreInitRadius,carnivoreInitHealth,carnivoreBonusHealthWhenEat, carnivoreReproductionThreshold, carnivoreHungrinessThreshold, carnivorePas)
		self.fourmieCreator = FourmieCreator(SCREEN_SIZE_X, SCREEN_SIZE_Y, nbFourmiPerColonie*nbFourmiColonie,fourmiInitRadius,fourmiInitHealth,fourmiBonusHealthWhenEat,fourmiReproductionThreshold,fourmiHungrinessThreshold,fourmiPas,  nbFourmiPerColonie,nbFourmiColonie, timeInEggForm, fourmiSenseRadius, fourmiNbRay, fourmiAngleOfVision)
		self.instance = Instance(SCREEN_SIZE_X, SCREEN_SIZE_Y,nbGrass,grassRadius,grassZoneEditRadius,bodyDecayingThreshold, self.herbivorCreator, self.carnivorCreator, self.fourmieCreator, positionObstacle)

		self._render = render


	def reset(self):
		self.rewards = []
		if self._render:
			self.display = Display(SCREEN_SIZE_X,SCREEN_SIZE_Y, self.motionService)
		self.herbivorCreator = HerbivorCreator(SCREEN_SIZE_X, SCREEN_SIZE_Y, nbHerbivore, herbivoreInitRadius,herbivoreInitHealth, herbivoreBonusHealthWhenEat, herbivoreReproductionThreshold, herbivoreHungrinessThreshold, herbivorePas)
		self.carnivorCreator = CarnivoreCreator(SCREEN_SIZE_X, SCREEN_SIZE_Y, nbCarnivore,carnivoreInitRadius,carnivoreInitHealth,carnivoreBonusHealthWhenEat, carnivoreReproductionThreshold, carnivoreHungrinessThreshold, carnivorePas)
		self.fourmieCreator = FourmieCreator(SCREEN_SIZE_X, SCREEN_SIZE_Y, nbFourmiPerColonie*nbFourmiColonie,fourmiInitRadius,fourmiInitHealth,fourmiBonusHealthWhenEat,fourmiReproductionThreshold,fourmiHungrinessThreshold,fourmiPas,  nbFourmiPerColonie,nbFourmiColonie, timeInEggForm, fourmiSenseRadius, fourmiNbRay, fourmiAngleOfVision)
		self.instance = Instance(SCREEN_SIZE_X, SCREEN_SIZE_Y,nbGrass,grassRadius,grassZoneEditRadius,bodyDecayingThreshold, self.herbivorCreator, self.carnivorCreator, self.fourmieCreator, positionObstacle)
		
		# Get the current state: array of (nb_agents, state_dim)
		self.current_state = []
		for fourmi in self.instance.fourmis:
			self.current_state.append(self.instance.getState(fourmi))
		self.current_state = np.array(self.current_state)
		return self.current_state

	def step(self, action):
		info = {}
		next_states = []
		rewards = []
		done = False
		self.instance.updateDish()
		next_states, rewards =  self.instance.cellsAct(action)
		self.updateCumulReward(rewards)		
		self.instance.isGoingThroughWall()
		self.render()
		return self.current_state, rewards, done, info
		


	def render(self):
		if self._render:
			self.display.displayAll(self.instance.herbivores,self.instance.carnivores,self.instance.fourmis,self.instance.dish, self.eventHandler, self.rewards)
			for e in pg.event.get():
				running = self.eventHandler.handleEvent(e,self.instance)

	def updateCumulReward(self, rewards) :
		if (len(self.rewards) == 0) :
			self.rewards.append(np.sum(rewards))
		else :
			self.rewards.append(np.sum(rewards) + self.rewards[-1])

	def close(self):
		if self._render:
			pg.quit()

	

    


