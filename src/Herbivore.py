import numpy as np

from src.Agent import EGreedy
from src.util import aColideWithB


class Herbivore:
    def __init__(self,x,y,dx,dy,r,g,b,radius,initHealth,bonusHealth,reproductionThreshold,pas):
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.r=r
        self.g=g
        self.b=b
        self.initialRadius=radius
        self.initHealth=initHealth
        self.bonusHealth=bonusHealth
        self.reproductionThreshold=reproductionThreshold
        self.health=initHealth
        self.radius=radius
        self.pas=pas
        self.nbOffspring=0
        self.nbAte=0
        self.hasEaten=False
        self.agent=EGreedy(2,1000)

    def run(self):
        self.x+=self.pas*self.dx
        self.y+=self.pas*self.dy
        self.normalize()

    def normalize(self):
        longueur = np.sqrt(self.dx **2  + self.dy**2 )
        self.dx /= longueur
        self.dy /= longueur

    def eat(self,grasses):
        self.hasEaten=False
        for grass in grasses:
            if aColideWithB(self.x,self.y,self.radius,grass.x,grass.y):
                grass.eaten()
                self.hasEaten=True
                self.health+=self.bonusHealth
                self.nbAte+=1

    def act(self,grasses):
        self.agent.play(self,grasses)

    def dying(self):
        self.health-=1
        self.radius = int(self.initialRadius*(self.health/self.initHealth))
        if self.radius>self.initialRadius:
            self.radius=self.initialRadius
        if self.radius<10:
            self.radius=10

    def shouldReproduce(self):
        if self.nbAte>=self.reproductionThreshold:
            self.nbAte=0
            self.nbOffspring+=1
            return True
        return False












