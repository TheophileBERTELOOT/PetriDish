import numpy as np

from src.Agent import EGreedy
from src.util import aColideWithB

class Fourmi:
    def __init__(self,x,y,dx,dy,r,g,b,radius,initHealth,bonusHealth,reproductionThreshold,hungrinessThreshold,pas,type,colonieId,TYPE_REINE,TYPE_OUVRIERE):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.r = r
        self.g = g
        self.b = b
        self.TYPE_REINE = TYPE_REINE
        self.TYPE_OUVRIERE=TYPE_OUVRIERE
        self.type=type
        self.initialRadius = radius
        self.colonieId=colonieId
        self.initHealth = initHealth
        self.bonusHealth = bonusHealth
        self.reproductionThreshold = reproductionThreshold
        self.hungrinessThreshold = hungrinessThreshold
        self.foodCarried = None
        self.probEatCarriedFood=0.0001
        self.hungriness = 0
        self.health = initHealth
        self.radius = radius
        self.pas = pas
        self.nbOffspring = 0
        self.nbAte = 0
        self.hasEaten = False
        self.agent = EGreedy(2, 1000)

    def run(self):
        if self.type!=self.TYPE_REINE:
            self.x += self.pas * self.dx
            self.y += self.pas * self.dy
            self.normalize()
            if self.foodCarried != None:
                self.foodCarried.x = self.x+((self.radius+2)*self.dx)
                self.foodCarried.y = self.y+((self.radius+2)*self.dy)


    def normalize(self):
        longueur = np.sqrt(self.dx ** 2 + self.dy ** 2)
        self.dx /= longueur
        self.dy /= longueur

    def eatCarriedFood(self):
        if self.foodCarried != None:
            if self.foodCarried.isEaten:
                self.foodCarried = None
            else:
                r = np.random.uniform()
                if r<self.probEatCarriedFood:
                    self.foodCarried.eaten()
                    self.foodCarried = None
                    self.hasEaten = True
                    self.health += self.bonusHealth
                    self.nbAte += 1
                    self.hungriness = 0
                elif r>self.probEatCarriedFood and r<50*self.probEatCarriedFood:
                    self.foodCarried.isCarried = False
                    self.foodCarried.x = self.x+self.radius*1.5*self.dx
                    self.foodCarried.y = self.y+self.radius*1.5*self.dy
                    self.foodCarried = None

    def eat(self, grasses):
        self.hasEaten = False
        for grass in grasses:
            if aColideWithB(self.x, self.y, self.radius, grass.x,
                            grass.y) and self.hungriness > self.hungrinessThreshold:
                r = np.random.uniform()
                if r <0.5 and self.foodCarried==None and self.type != self.TYPE_REINE:
                    self.foodCarried = grass
                    grass.carried(self.x,self.y)
                else:
                    if (self.foodCarried !=None and self.foodCarried != grass) or self.foodCarried == None:
                        grass.eaten()
                        self.hasEaten = True
                        self.health += self.bonusHealth
                        self.nbAte += 1
                        self.hungriness = 0
        if not self.hasEaten:
            self.hungriness += 1

    def act(self, grasses):
        self.agent.play(self, grasses)

    def dying(self):
        self.health -= 1
        self.radius = int(self.initialRadius * (self.health / self.initHealth))
        if self.radius > self.initialRadius:
            self.radius = self.initialRadius
        if self.radius < 10:
            self.radius = 10

    def shouldReproduce(self):
        if self.nbAte >= self.reproductionThreshold and self.type == self.TYPE_REINE:
            self.nbAte = 0
            self.nbOffspring += 1
            return True
        return False


