from gym_ants.environment.Dish import Dish
from gym_ants.species import Herbivore, Fourmi, Carnivore
from gym_ants.species import FourmiType
from gym_ants.environment.Obstacle import Obstacle
import random
import numpy as np
import pygame as pg

from copy import deepcopy



class Instance(object):

    def __init__(self,maxX,maxY,nbGrass,grassRadius,grassZoneEditRadius,bodyDecayingThreshold, herbivorCreator, carnivorCreator, fourmieCreator, positionsObstacle):
        
        
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
        self.oldClosestFood = None
        self.oldType = []
        queen_ants = self.getQueenAnt()
        self.dish = Dish(maxX,maxY,nbGrass,grassRadius,grassZoneEditRadius, positionsObstacle, queen_ants)


    def getQueenAnt(self):
        queens = []
        for ant in self.fourmis :
            if (ant.type == FourmiType.REINE) :
                queens.append(ant)
        return queens


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
                food = self.dish.grasses + self.deadBodies
                for antHill in self.dish.antHills:
                    if antHill.colonieId == fourmi.colonieId:
                        fourmiAntHill = antHill

                if (fourmi.type == FourmiType.OUVRIERE) :
                    self.applyAction(fourmi, actions[fourmiIndex], food)
                    self.oldType = deepcopy(fourmi.visionRayObject)
                    self.oldDistance = deepcopy(fourmi.visionRayLength)
                else:
                    fourmi.QeenEat(food,antHill,self.fourmis)

                if (self.dish.isGoingThroughObstacles(fourmi)) :
                    fourmi.deviate_obstacles()
                else :
                    fourmi.run()
                fourmi.interaction_between_colonies(self.fourmis)
                fourmi.dying()
                fourmi.isHatched()
                fourmi.smell(self.fourmis,self.dish.grasses, self.obstacles)
                if fourmi.type == FourmiType.REINE:
                    if fourmi.shouldReproduce():
                        newBorn = self.fourmieCreator.Create(parent=fourmi)
                        newBorn.isEgg = True
                        newBorns.append(newBorn)

            else:
                if fourmi not in self.deadBodies:
                    fourmi.radius = self.grassRadius
                    fourmi.r = 255
                    fourmi.g = 0
                    fourmi.b = 0
                    fourmi.color = pg.Color((255,0,0))
                    self.deadBodies.append(fourmi)
                if fourmi.health < self.bodyDecayingThreshold or fourmi.isEaten:
                    fourmiToRemove.append(fourmi)


            rewards.append(self._get_reward(fourmi))
            next_states.append(self.getState(fourmi))
        self.fourmis += newBorns

        for fourmi in fourmiToRemove:
            if fourmi in self.deadBodies:
                self.deadBodies.remove(fourmi)
            if fourmi in self.fourmis:
                self.fourmis.remove(fourmi)

        return np.array(next_states), np.array(rewards)


    def getClosestFoodCoordinate(self,cell):
        minDist = np.sqrt(self.maxX ** 2 + self.maxY ** 2)
        index = 0
        if len(cell.objectInVisionDistance) > 0:
            minDist = min(cell.objectInVisionDistance)
            index = cell.objectInVisionDistance.index(minDist)
            return cell.objectInVisionRange[index].coordinate


        return [-1,-1]

    def closestFood(self,cell):
        minDist = np.sqrt(self.maxX**2 + self.maxY**2)
        if len(cell.objectInVisionDistance)>0:
            minDist = min(cell.objectInVisionDistance)


        return  minDist

    def closestEnemy(self, cell):
        minDist = np.sqrt(self.maxX**2 + self.maxY**2)
        if len(cell.enemyInVisionDistance)>0:
            minDist = min(cell.enemyInVisionDistance)
        return minDist

    def closestObstacle(self, cell):
        minDist = np.sqrt(self.maxX**2 + self.maxY**2)
        if len(cell.obstacleInVisionDistance)>0:
            minDist = min(cell.obstacleInVisionDistance)
        return minDist



    def calcDistanceReward(self,cell):
        closestFood = self.closestFood(cell)
        if self.oldClosestFood:
            if closestFood<self.oldClosestFood:
                self.oldClosestFood = closestFood
                return 10
        self.oldClosestFood = closestFood
        return - 5

    def _get_reward(self, cell):
        if cell.hasEaten:
            reward = 1000
        else:
            reward = self.calcDistanceReward(cell)
        return reward


    def applyAction(self, cell, selectedAction, food):

        angle = cell.angle

        if selectedAction == 0:
            angle+=np.pi/12
            cell.dx = np.cos(angle)
            cell.dy = np.sin(angle)
            cell.normalize()
        elif selectedAction== 1:
            angle-=np.pi/12
            cell.dx = np.cos(angle)
            cell.dy = np.sin(angle)
            cell.normalize()
        elif selectedAction== 2:
            angle = angle
            cell.normalize()

        elif selectedAction == 3:
            cell.eat(food)
        elif selectedAction == 4:
            cell.carryFood(food)
        elif selectedAction == 5:
            cell.dropCarriedFood()
            
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

    def getState(self, cell):
        # return np.array([cell.coordinate[0], cell.coordinate[1], cell.health, self.closestFood(cell), self.closestObstacle(cell), self.closestEnemy(cell)])
        closestFoodCoordinate = self.getClosestFoodCoordinate(cell)
        return np.array([cell.coordinate[0], cell.coordinate[1],closestFoodCoordinate[0],closestFoodCoordinate[1]])





