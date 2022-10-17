import numpy as np

from src.Agent import EGreedy
from src.util import aColideWithB


class Carnivore:
    def __init__(self,x,y,dx,dy,r,g,b,radius,initHealth,bonusHealth,reproductionThreshold,hungrinessThreshold,pas):
        self.coordinate=np.array([x,y],dtype=float)
        self.dx=dx
        self.dy=dy
        self.r=r
        self.g=g
        self.b=b
        self.initialRadius=radius
        self.initHealth=initHealth
        self.bonusHealth=bonusHealth
        self.reproductionThreshold=reproductionThreshold
        self.hungrinessThreshold=hungrinessThreshold
        self.hungriness=0
        self.health=initHealth
        self.radius=radius
        self.pas=pas
        self.nbOffspring=0
        self.nbAte=0
        self.hasEaten=False
        self.agent=EGreedy(2,1000)

    def run(self):
        self.coordinate[0]+=self.pas*self.dx
        self.coordinate[1]+=self.pas*self.dy
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












