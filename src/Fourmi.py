import numpy as np

from src.Agent import EGreedy
from src.util import aColideWithB,lineColideWithCircle,calcDistanceBetweenTwoPoint

class Fourmi:
    def __init__(self,x,y,dx,dy,r,g,b,radius,initHealth,bonusHealth,reproductionThreshold,hungrinessThreshold,pas,timeInEggForm,fourmiSenseRadius,fourmiNbRay,type,colonieId,TYPE_REINE,TYPE_OUVRIERE):
        self.coordinate=np.array([x,y],dtype=float)
        self.dx = dx
        self.dy = dy
        self.r = r
        self.g = g
        self.b = b
        self.TYPE_REINE = TYPE_REINE
        self.TYPE_OUVRIERE=TYPE_OUVRIERE
        self.timeInEggForm=timeInEggForm
        self.type=type
        self.initialRadius = radius
        self.colonieId=colonieId
        self.initHealth = initHealth
        self.bonusHealth = bonusHealth
        self.reproductionThreshold = reproductionThreshold
        self.hungrinessThreshold = hungrinessThreshold
        self.foodCarried = None
        self.probEatCarriedFood=0.0001
        self.age = 0
        self.isEgg=False
        self.hungriness = 0
        self.health = initHealth
        self.radius = radius
        self.pas = pas
        self.nbOffspring = 0
        self.nbAte = 0
        self.hasEaten = False
        self.fourmiSenseRadius = fourmiSenseRadius
        self.fourmiNbRay=fourmiNbRay
        self.agent = EGreedy(2, 1000)
        self.visionRayCoordinate = []
        anglePerRay = 2*np.pi/self.fourmiNbRay
        lengthRay = self.fourmiSenseRadius + self.radius
        for indexRay in range(self.fourmiNbRay):
            x = self.coordinate[0] + lengthRay * (np.cos(anglePerRay * indexRay))
            y = self.coordinate[1] + lengthRay * (np.sin(anglePerRay * indexRay))
            self.visionRayCoordinate.append([x,y])
        self.visionRayCoordinate = np.array(self.visionRayCoordinate)


    def run(self):
        if self.type!=self.TYPE_REINE and not self.isEgg:
            self.coordinate[0] += self.pas * self.dx
            self.coordinate[1] += self.pas * self.dy
            self.normalize()
            if self.foodCarried != None:
                self.foodCarried.x = self.coordinate[0]+((self.radius+2)*self.dx)
                self.foodCarried.y = self.coordinate[1]+((self.radius+2)*self.dy)


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
                    self.foodCarried.x = self.coordinate[0]+self.radius*1.5*self.dx
                    self.foodCarried.y = self.coordinate[1]+self.radius*1.5*self.dy
                    self.foodCarried = None

    def smell(self,fourmis):
        anglePerRay = 2 * np.pi / self.fourmiNbRay
        lengthRay = self.fourmiSenseRadius + self.radius
        for indexRay in range(self.fourmiNbRay):
            L = self.visionRayCoordinate[indexRay]
            E = self.coordinate
            isColidingOnce = False
            for fourmi in fourmis:
                if fourmi != self:
                    C = fourmi.coordinate
                    r = fourmi.radius
                    isColiding = lineColideWithCircle(L,E,C,r)
                    if isColiding :
                        lengthRay = calcDistanceBetweenTwoPoint(E,C)-r
                        self.visionRayCoordinate[indexRay][0] = self.coordinate[0] +  lengthRay* (np.cos(anglePerRay * indexRay))
                        self.visionRayCoordinate[indexRay][1] = self.coordinate[1] + lengthRay * (
                            np.sin(anglePerRay * indexRay))
                        isColidingOnce = True
                        break
            if not isColidingOnce:
                lengthRay = self.fourmiSenseRadius + self.radius
                self.visionRayCoordinate[indexRay][0] = self.coordinate[0] + lengthRay * (
                    np.cos(anglePerRay * indexRay))
                self.visionRayCoordinate[indexRay][1] = self.coordinate[1] + lengthRay * (
                    np.sin(anglePerRay * indexRay))




    def eat(self, grasses):
        self.hasEaten = False
        for grass in grasses:
            if aColideWithB(self.coordinate[0], self.coordinate[1], self.radius, grass.coordinate[0],
                            grass.coordinate[1]) and self.hungriness > self.hungrinessThreshold:
                r = np.random.uniform()
                if r <0.5 and self.foodCarried==None and self.type != self.TYPE_REINE and not self.isEgg:
                    self.foodCarried = grass
                    grass.carried(self.coordinate[0],self.coordinate[1])
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

    def isHatched(self):
        if self.age >= self.timeInEggForm and self.nbAte>=self.reproductionThreshold and self.isEgg:
            self.isEgg = False
            self.age = 0

    def dying(self):
        self.health -= 1
        if self.isEgg :
            self.age+=1
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


