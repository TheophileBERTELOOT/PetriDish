from src.Dish import Dish
from src.Grass import Grass
from src.Herbivore import Herbivore
import random
import numpy as np

class Instance:
    def __init__(self,nbHerbivore,maxX,maxY,herbiboreInitRadius,herbivoreInitHealth,herbivoreBonusHealthWhenEat,herbivorePas,nbGrass,grassRadius):
        self.dish = Dish(maxX,maxY)
        self.nbHerbivore = nbHerbivore
        self.maxX=maxX
        self.maxY=maxY
        self.herbivoreInitRadius=herbiboreInitRadius
        self.herbivoreInitHealth=herbivoreInitHealth
        self.herbivoreBonusHealthWhenEat=herbivoreBonusHealthWhenEat
        self.grassRadius=grassRadius
        self.herbivores = []
        self.grasses=[]
        self.nbGrass=nbGrass
        self.herbivorePas=herbivorePas
        self.initHerbivores()
        self.initGrasses()


    def initHerbivores(self):
        for _ in range(self.nbHerbivore):
            x = random.randint(0,self.maxX)
            y = random.randint(0,self.maxY)
            angle = random.randint(0,self.maxX)
            dx = np.cos(angle)
            dy = np.sin(angle)
            r = random.randint(0,255)
            g = 255
            b = random.randint(0,255)
            radius = self.herbivoreInitRadius
            health = self.herbivoreInitHealth
            bonusHealth=self.herbivoreBonusHealthWhenEat
            pas = self.herbivorePas
            herbivore = Herbivore(x,y,dx,dy,r,g,b,radius,health,bonusHealth,pas)
            self.herbivores.append(herbivore)

    def initGrasses(self):
        for _ in range(self.nbGrass):
            x = random.randint(0, self.maxX)
            y = random.randint(0, self.maxY)
            radius= self.grassRadius
            grass = Grass(x,y,radius,self.maxX,self.maxY)
            self.grasses.append(grass)



    def herbivoresAct(self):
        herbivoreDead=[]
        for herbivoreIndex in range(len(self.herbivores)):
            herbivore = self.herbivores[herbivoreIndex]
            if herbivore.health > 0:
                herbivore.act(self.grasses)
                herbivore.run()
                herbivore.dying()




    def isGoingThroughWall(self):
        self.dish.isGoingThroughWall(self.herbivores)



