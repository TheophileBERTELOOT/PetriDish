import numpy as np

from src.Agent import EGreedy
from src.util import aColideWithB
from src.species.Species import Species

class Carnivore(Species):
    def __init__(self,x,y,dx,dy,r,g,b,radius,initHealth,bonusHealth,reproductionThreshold,hungrinessThreshold,pas):
        super().__init__(x,y,dx,dy,r,g,b,radius,initHealth,bonusHealth,reproductionThreshold,hungrinessThreshold,pas)

        self.agent=EGreedy(2,1000)

    def run(self):
        self.coordinate[0]+=self.pas*self.dx
        self.coordinate[1]+=self.pas*self.dy
        self.normalize()

    def deviate_obstacles(self) :
        self.coordinate[0]-= 1/2 * self.pas*self.dx
        self.coordinate[1]-=1/2 * self.pas*self.dy
        self.normalize()

    def normalize(self):
        longueur = np.sqrt(self.dx **2  + self.dy**2 )
        self.dx /= longueur
        self.dy /= longueur

    def eat(self,herbivores):
        self.hasEaten=False
        for herbivore in herbivores:
            if aColideWithB(self.coordinate[0],self.coordinate[1],self.radius,herbivore.coordinate[0],herbivore.coordinate[1]) and herbivore.health>0 and self.hungriness>self.hungrinessThreshold:
                herbivore.health = 0
                self.hasEaten=True
                self.health+=self.bonusHealth
                self.nbAte+=1
                self.hungriness=0
        if not self.hasEaten:
            self.hungriness+=1

    def act(self,herbivores):
        self.agent.play(self,herbivores)

    def dying(self):
        self.health-=1
        self.radius = int(self.initialRadius*(self.health/self.initHealth))
        if self.radius>self.initialRadius:
            self.radius=self.initialRadius
        if self.radius<10:
            self.radius=10

    def shouldReproduce(self,carnivores):
        for carnivore in carnivores:
            if carnivore != self:
                if aColideWithB(self.coordinate[0],self.coordinate[1],self.radius,carnivore.coordinate[0],carnivore.coordinate[1]):
                    if self.nbAte>=self.reproductionThreshold:
                        self.nbAte=0
                        self.nbOffspring+=1
                        return True
        return False












