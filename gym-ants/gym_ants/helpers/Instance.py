from gym_ants.environment.Dish import Dish
from gym_ants.species import Herbivore, Fourmi, Carnivore
from gym_ants.species import FourmiType
from gym_ants.environment.Obstacle import Obstacle
import random
import numpy as np
from copy import deepcopy


class Instance(object):

    def __init__(self,maxX,maxY,nbGrass,grassRadius,grassZoneEditRadius,bodyDecayingThreshold, herbivorCreator, carnivorCreator, fourmieCreator, positionObstacle):
        
        
        self.dish = Dish(maxX,maxY,nbGrass,grassRadius,grassZoneEditRadius, positionObstacle)
        self.maxX=maxX
        self.maxY=maxY

        self.grassRadius=grassRadius
        self.nbGrass=nbGrass

        self.bodyDecayingThreshold=bodyDecayingThreshold
        self.herbivorCreator = herbivorCreator
        self.carnivorCreator = carnivorCreator
        self.fourmieCreator = fourmieCreator

        self.grassZoneEditRadius = grassZoneEditRadius
        self.herbivores = self.herbivorCreator.initSpecies()
        self.carnivores = self.carnivorCreator.initSpecies()
        self.fourmis = self.fourmieCreator.initSpecies()
        
        self.obstacles = []

        self.deadBodies = []

        self.grassEditMode = False

        self.old_value = 0
        self.old_action = 0
        self.oldDistance = []
        self.oldType = []

        #self.agents = {}
        #self.initAgents()




    """def initAgents(self):
        if len(self.fourmis)>0:
            self.agents['fourmis'] = Qlearning(3,self.fourmis[0].fourmiNbRay,2)"""

    def herbivoresAct(self):
        newBorns=[]
        for herbivoreIndex in range(len(self.herbivores)):
            herbivore = self.herbivores[herbivoreIndex]
            if herbivore.health > 0:
                herbivore.act(self.dish.grasses)
                if (self.dish.isGoingThroughObstacles(herbivore)) :
                    herbivore.deviate_obstacles()
                else :
                    herbivore.run()
                herbivore.dying()
                if herbivore.shouldReproduce():
                    deadHerbivoreFound=False
                    for deadHerbivoreIndex in range(len(self.herbivores)):
                        deadHerbivore=self.herbivores[deadHerbivoreIndex]
                        if deadHerbivore.health<0:
                            self.herbivores[deadHerbivoreIndex] = self.initHerbivore(herbivore)
                            deadHerbivoreFound =True
                            break
                    if not deadHerbivoreFound:
                        newBorn=self.herbivorCreator.create(herbivore)
                        newBorns.append(newBorn)
        self.herbivores+=newBorns

    def carnivoresAct(self):
        newBorns=[]
        for carnivoreIndex in range(len(self.carnivores)):
            carnivore = self.carnivores[carnivoreIndex]
            if carnivore.health > 0:
                carnivore.act(self.herbivores)
                if (self.dish.isGoingThroughObstacles(carnivore)) :
                    carnivore.deviate_obstacles()
                else :
                    carnivore.run()
                carnivore.dying()
                if carnivore.shouldReproduce(self.carnivores):
                    deadCarnivoreFound=False
                    for deadCarnivoreIndex in range(len(self.carnivores)):
                        deadCarnivore=self.carnivores[deadCarnivoreIndex]
                        if deadCarnivore.health<0:
                            self.carnivores[deadCarnivoreIndex] = self.initCarnivore(carnivore)
                            deadCarnivoreFound =True
                            break
                    if not deadCarnivoreFound:
                        newBorn=self.carnivorCreator.create(carnivore)
                        newBorns.append(newBorn)
        self.carnivores+=newBorns


    def fourmisAct(self, actions):
        newBorns=[]
        fourmiToRemove=[]
        rewards, next_states = [], []

        for fourmiIndex in range(len(self.fourmis)):
            fourmi = self.fourmis[fourmiIndex]
            if fourmi.health > 0:
                if (fourmi.type == FourmiType.OUVRIERE) :
                    food = self.dish.grasses + self.deadBodies
                    #  self.agents['fourmis'].play(fourmi,food)
                    fourmi.eat(food)
                    self.applyAction(actions[fourmiIndex])
                    self.oldType = copy.deepcopy(fourmi.visionRayObject)
                    self.oldDistance = copy.deepcopy(fourmi.visionRayLength)
                    

                fourmi.eatCarriedFood()
                if (self.dish.isGoingThroughObstacles(fourmi)) :
                    fourmi.deviate_obstacles()
                else :
                    fourmi.run()
                fourmi.interaction_between_colonies(self.fourmis)
                fourmi.dying()
                fourmi.isHatched()
                fourmi.smell(self.fourmis,self.dish.grasses)
                if fourmi.type == FourmiType.REINE:
                    if fourmi.shouldReproduce():
                        newBorn = self.fourmieCreator.create(parent=fourmi)
                        newBorn.isEgg = True
                        newBorns.append(newBorn)
                    self.fourmis += newBorns
            else:
                if fourmi not in self.deadBodies:
                    self.deadBodies.append(fourmi)
                    fourmi.radius = self.grassRadius
                    fourmi.r = 255
                    fourmi.g = 0
                    fourmi.b = 0
                if fourmi.health < self.bodyDecayingThreshold:
                    fourmiToRemove.append(fourmi)

            rewards.append(self._get_reward(fourmi))
            next_states.append(self.stateFromRayType(fourmi))

        for fourmi in fourmiToRemove:
            self.fourmis.remove(fourmi)
            self.deadBodies.remove(fourmi)
        return np.array(next_states), np.array(rewards)

        

    def calcDistanceReward(self,cell):
        for indexRay in range(len(self.oldDistance)):
            newType = cell.visionRayObject[indexRay]
            oldRayType = self.oldType[indexRay]
            if newType == 1:
                newDistance = cell.visionRayLength[indexRay]
                oldRayDistance = self.oldDistance[indexRay]
                if newDistance<oldRayDistance:
                    return 50

    def _get_reward(self, cell):
        if cell.hasEaten:
            reward = 1000
        else:
            return self.calcDistanceReward(cell)


    def applyAction(self, cell, selectedAction):
        angle = cell.angle

        if selectedAction == 0:
            angle+=np.pi/12
            cell.dx = np.cos(angle)
            cell.dy = np.sin(angle)
        elif selectedAction == 1:
            angle-=np.pi/12
            cell.dx = np.cos(angle)
            cell.dy = np.sin(angle)
        else:
            angle = angle
        cell.normalize()

    def cellsAct(self, actions):
        self.herbivoresAct()
        self.carnivoresAct()
        next_states, rewards = self.fourmisAct(actions)
        return next_states, rewards

    def updateDish(self):
        self.dish.regrowEatenGrasses()

    def isGoingThroughWall(self):
        self.dish.isGoingThroughWall(self.herbivores+self.carnivores+self.fourmis)

    def stateFromRayType(self,rayType):
        for rayIndex in range(len(rayType)):
            ray = rayType[rayIndex]
            if ray == 1:
                return np.array([rayIndex+1])
        return np.array([0])






