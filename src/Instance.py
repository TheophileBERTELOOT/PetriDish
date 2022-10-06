from src.Dish import Dish
from src.Grass import Grass
from src.Herbivore import Herbivore
from src.Fourmi import Fourmi
from src.Carnivore import Carnivore
import random
import numpy as np
from copy import deepcopy

class Instance:
    def __init__(self,nbHerbivore,maxX,maxY,
                 herbiboreInitRadius,herbivoreInitHealth,herbivoreBonusHealthWhenEat,herbivoreReproductionThreshold,herbivoreHungrinessThreshold,
                 nbCarnivore,carnivoreInitRadius,carnivoreInitHealth,carnivoreBonusHealthWhenEat,carnivoreReproductionThreshold,carnivoreHungrinessThreshold,
                 nbFourmiPerColonie,nbFourmiColonie, fourmiInitRadius, fourmiInitHealth, fourmiBonusHealthWhenEat, fourmiReproductionThreshold,
                 fourmiHungrinessThreshold,
                 herbivorePas,carnivorePas,fourmiPas,nbGrass,grassRadius,grassZoneEditRadius):
        self.dish = Dish(maxX,maxY,nbGrass,grassRadius,grassZoneEditRadius)

        self.maxX=maxX
        self.maxY=maxY

        self.herbivoreInitRadius=herbiboreInitRadius
        self.herbivoreInitHealth=herbivoreInitHealth
        self.herbivoreBonusHealthWhenEat=herbivoreBonusHealthWhenEat
        self.herbivoreReproductionThreshold=herbivoreReproductionThreshold
        self.herbivoreHungrinessThreshold=herbivoreHungrinessThreshold

        self.carnivoreInitRadius=carnivoreInitRadius
        self.carnivoreInitHealth=carnivoreInitHealth
        self.carnivoreBonusHealthWhenEat=carnivoreBonusHealthWhenEat
        self.carnivoreReproductionThreshold=carnivoreReproductionThreshold
        self.carnivoreHungrinessThreshold=carnivoreHungrinessThreshold

        self.fourmiInitRadius=fourmiInitRadius
        self.fourmiInitHealth=fourmiInitHealth
        self.fourmiBonusHealthWhenEat=fourmiBonusHealthWhenEat
        self.fourmiReproductionThreshold=fourmiReproductionThreshold
        self.fourmiHungrinessThreshold=fourmiHungrinessThreshold

        self.grassRadius=grassRadius
        self.nbGrass=nbGrass
        self.nbHerbivore = nbHerbivore
        self.nbCarnivore=nbCarnivore
        self.nbFourmiPerColonie=nbFourmiPerColonie
        self.nbFourmiColonie=nbFourmiColonie
        self.herbivorePas=herbivorePas
        self.carnivorePas=carnivorePas
        self.fourmiPas=fourmiPas

        self.grassZoneEditRadius = grassZoneEditRadius
        self.herbivores = []
        self.carnivores = []
        self.fourmis=[]


        self.grassEditMode = False

        self.initHerbivores()
        self.initCarnivores()
        self.initFourmis()


    def initHerbivore(self,parent=None):
        if parent == None:
            x = random.randint(0, self.maxX)
            y = random.randint(0, self.maxY)
            angle = random.randint(0, self.maxX)
            dx = np.cos(angle)
            dy = np.sin(angle)
            r = random.randint(0, 255)
            g = 255
            b = random.randint(0, 255)
            radius = self.herbivoreInitRadius
            health = self.herbivoreInitHealth
            bonusHealth = self.herbivoreBonusHealthWhenEat
            reproductionThreshold = self.herbivoreReproductionThreshold
            hungrinessThreshold = self.herbivoreHungrinessThreshold
            pas = self.herbivorePas
            herbivore = Herbivore(x, y, dx, dy, r, g, b, radius, health, bonusHealth, reproductionThreshold,hungrinessThreshold, pas)
        else:
            x = parent.x
            y = parent.y
            angle = random.randint(0, self.maxX)
            dx = np.cos(angle)
            dy = np.sin(angle)
            r = parent.r
            g = 255
            b = parent.b
            radius = self.herbivoreInitRadius
            health = self.herbivoreInitHealth
            bonusHealth = self.herbivoreBonusHealthWhenEat
            reproductionThreshold = self.herbivoreReproductionThreshold
            pas = self.herbivorePas
            hungrinessThreshold = self.herbivoreHungrinessThreshold
            herbivore = Herbivore(x, y, dx, dy, r, g, b, radius, health, bonusHealth, reproductionThreshold,hungrinessThreshold, pas)
            herbivore.agent = deepcopy(parent.agent)
        return herbivore

    def initHerbivores(self):
        for _ in range(self.nbHerbivore):
            herbivore = self.initHerbivore()
            self.herbivores.append(herbivore)


    def initCarnivore(self, parent=None):
        if parent == None:
            x = random.randint(0, self.maxX)
            y = random.randint(0, self.maxY)
            angle = random.randint(0, self.maxX)
            dx = np.cos(angle)
            dy = np.sin(angle)
            r = 255
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            radius = self.carnivoreInitRadius
            health = self.carnivoreInitHealth
            bonusHealth = self.carnivoreBonusHealthWhenEat
            reproductionThreshold = self.carnivoreReproductionThreshold
            hungrinessThreshold = self.carnivoreHungrinessThreshold
            pas = self.carnivorePas
            carnivore = Carnivore(x, y, dx, dy, r, g, b, radius, health, bonusHealth, reproductionThreshold,hungrinessThreshold, pas)
        else:
            x = parent.x
            y = parent.y
            angle = random.randint(0, self.maxX)
            dx = np.cos(angle)
            dy = np.sin(angle)
            r = 255
            g = parent.g
            b = parent.b
            radius = self.carnivoreInitRadius
            health = self.carnivoreInitHealth
            bonusHealth = self.carnivoreBonusHealthWhenEat
            reproductionThreshold = self.carnivoreReproductionThreshold
            hungrinessThreshold = self.carnivoreHungrinessThreshold
            pas = self.carnivorePas
            carnivore = Carnivore(x, y, dx, dy, r, g, b, radius, health, bonusHealth, reproductionThreshold,hungrinessThreshold, pas)
            carnivore.agent = deepcopy(parent.agent)
        return carnivore

    def initCarnivores(self):
        for _ in range(self.nbCarnivore):
            carnivore = self.initCarnivore()
            self.carnivores.append(carnivore)

    def initFourmi(self,parent=None,colonieId=0,color=()):
        if parent == None:
            x = random.randint(0, self.maxX)
            y = random.randint(0, self.maxY)
            angle = random.randint(0, self.maxX)
            dx = np.cos(angle)
            dy = np.sin(angle)
            radius = self.fourmiInitRadius
            health = self.fourmiInitHealth
            bonusHealth = self.fourmiBonusHealthWhenEat
            reproductionThreshold = self.fourmiReproductionThreshold
            hungrinessThreshold = self.fourmiHungrinessThreshold
            pas = self.fourmiPas
            fourmi = Fourmi(x, y, dx, dy, color[0],color[1],color[2], radius, health, bonusHealth, reproductionThreshold,hungrinessThreshold, pas,0,colonieId)
        else:
            x = parent.x
            y = parent.y
            angle = random.randint(0, self.maxX)
            dx = np.cos(angle)
            dy = np.sin(angle)
            r = parent.r
            g = 255
            b = parent.b
            radius = self.fourmiInitRadius
            health = self.fourmiInitHealth
            bonusHealth = self.fourmiBonusHealthWhenEat
            reproductionThreshold = self.fourmiReproductionThreshold
            pas = self.fourmiPas
            hungrinessThreshold = self.fourmiHungrinessThreshold
            colonieId= parent.colonieId
            fourmi = Fourmi(x, y, dx, dy, r, g, b, radius, health, bonusHealth, reproductionThreshold,hungrinessThreshold, pas,0,colonieId)
            fourmi.agent = deepcopy(parent.agent)
        return fourmi


    def initFourmis(self):
        for colonieId in range(self.nbFourmiColonie):
            r = random.randint(0, 100)
            g = random.randint(0, 100)
            b = random.randint(0, 100)
            colonieColor = (r,g,b)
            for _ in range(self.nbFourmiPerColonie):
                fourmi = self.initFourmi(colonieId=colonieId,color=colonieColor)
                self.fourmis.append(fourmi)

    def herbivoresAct(self):
        newBorns=[]
        for herbivoreIndex in range(len(self.herbivores)):
            herbivore = self.herbivores[herbivoreIndex]
            if herbivore.health > 0:
                herbivore.act(self.dish.grasses)
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
                        newBorn=self.initHerbivore(herbivore)
                        newBorns.append(newBorn)
        self.herbivores+=newBorns

    def carnivoresAct(self):
        newBorns=[]
        for carnivoreIndex in range(len(self.carnivores)):
            carnivore = self.carnivores[carnivoreIndex]
            if carnivore.health > 0:
                carnivore.act(self.herbivores)
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
                        newBorn=self.initCarnivore(carnivore)
                        newBorns.append(newBorn)
        self.carnivores+=newBorns


    def fourmisAct(self):
        newBorns=[]
        for fourmiIndex in range(len(self.fourmis)):
            fourmi = self.fourmis[fourmiIndex]
            if fourmi.health > 0:
                fourmi.act(self.dish.grasses)
                fourmi.eatCarriedFood()
                fourmi.run()
                fourmi.dying()



    def cellsAct(self):
        self.herbivoresAct()
        self.carnivoresAct()
        self.fourmisAct()

    def updateDish(self):
        self.dish.regrowEatenGrasses()

    def isGoingThroughWall(self):
        self.dish.isGoingThroughWall(self.herbivores+self.carnivores)







