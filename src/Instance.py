from .Dish import Dish
from src.species import Herbivore, Fourmi, Carnivore
from src.species import FourmiType
from src.Obstacle import Obstacle
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


    def fourmisAct(self):
        newBorns=[]
        fourmiToRemove=[]
        for fourmiIndex in range(len(self.fourmis)):
            fourmi = self.fourmis[fourmiIndex]
            if fourmi.health > 0:
                fourmi.act(self.dish.grasses,self.deadBodies)
                fourmi.eatCarriedFood()
                if (self.dish.isGoingThroughObstacles(fourmi)) :
                    fourmi.deviate_obstacles()
                else :
                    fourmi.run()
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
        for fourmi in fourmiToRemove:
            self.fourmis.remove(fourmi)
            self.deadBodies.remove(fourmi)


    def cellsAct(self):
        self.herbivoresAct()
        self.carnivoresAct()
        self.fourmisAct()

    def updateDish(self):
        self.dish.regrowEatenGrasses()

    def isGoingThroughWall(self):
        self.dish.isGoingThroughWall(self.herbivores+self.carnivores+self.fourmis)







