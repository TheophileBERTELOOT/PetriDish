import numpy as np
import pygame as pg
from enum import Enum

from gym_ants.species.Species import Species
from src.Agent import EGreedy
from gym_ants.helpers.util import aColideWithB,lineColideWithCircle,calcDistanceBetweenTwoPoint,calcAngle
from src.Qlearning import Qlearning

class FourmiType(Enum) :
    REINE = 0
    OUVRIERE = 1



class Fourmi(Species):
    def __init__(self,x,y,dx,dy,r,g,b,radius,initHealth,bonusHealth,reproductionThreshold,hungrinessThreshold,pas,timeInEggForm,
                 fourmiSenseRadius,fourmiNbRay,fourmiAngleOfVision,type,colonieId, avgLifeExpectancy = 1000, seed=42):
        super().__init__(x,y,dx,dy,r,g,b,radius,initHealth,bonusHealth,reproductionThreshold,hungrinessThreshold,pas)

        self.color = pg.Color((r,g,b))

        self.type=type
        self.colonieId=colonieId

        self.foodCarried = None
        self.probEatCarriedFood=0.0001
        self.age = -timeInEggForm
        self.isEgg=False
        self.hungriness = 0
        
        self.isCarried=False
        self.isEaten = False
        self.fourmiSenseRadius = fourmiSenseRadius
        self.fourmiNbRay=fourmiNbRay
        self.fourmiAngleOfVision =fourmiAngleOfVision
        # self.agent = EGreedy(2, 1000)
        self.agent = Qlearning(3,self.fourmiNbRay,2)
        self.visionRayCoordinate = []
        self.visionRayLength = []
        self.visionRayObject = []
        anglePerRay = 2*np.pi/self.fourmiNbRay
        lengthRay = self.fourmiSenseRadius + self.radius

        for indexRay in range(self.fourmiNbRay):
            x = self.coordinate[0] + lengthRay * (np.cos(anglePerRay * indexRay))
            y = self.coordinate[1] + lengthRay * (np.sin(anglePerRay * indexRay))
            self.visionRayCoordinate.append([x,y])
            self.visionRayLength.append(lengthRay)
            self.visionRayObject.append(None)
        self.visionRayCoordinate = np.array(self.visionRayCoordinate)
        self.random = np.random.RandomState()
        self.death_age = self.random.exponential(avgLifeExpectancy)
        self.angle = calcAngle(self.dx,self.dy)


    def run(self):
        if self.type!=FourmiType.REINE and not self.isEgg:
            self.coordinate[0] += self.pas * self.dx
            self.coordinate[1] += self.pas * self.dy
            self.normalize()
            if self.foodCarried != None:
                self.foodCarried.x = self.coordinate[0]+((self.radius+2)*self.dx)
                self.foodCarried.y = self.coordinate[1]+((self.radius+2)*self.dy)

    def deviate_obstacles(self) :
        self.coordinate[0]-= 1/2 * self.pas*self.dx
        self.coordinate[1]-=1/2 * self.pas*self.dy
        self.normalize()
        if self.foodCarried != None:
            self.foodCarried.x = self.coordinate[0]+((self.radius+2)*self.dx)
            self.foodCarried.y = self.coordinate[1]+((self.radius+2)*self.dy)


    def normalize(self):
        longueur = np.sqrt(self.dx ** 2 + self.dy ** 2)
        self.dx /= longueur
        self.dy /= longueur
        self.angle = calcAngle(self.dx,self.dy)


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

    def updateVisionRay(self,indexRay,L,E,C,r,type):
        anglePerRay = self.fourmiAngleOfVision / self.fourmiNbRay
        lengthRay = calcDistanceBetweenTwoPoint(E, C)
        self.visionRayCoordinate[indexRay][0] = self.coordinate[0] + lengthRay * (np.cos(1.5*self.angle  + anglePerRay * indexRay))
        self.visionRayCoordinate[indexRay][1] = self.coordinate[1] + lengthRay * (
            np.sin(1.5*self.angle + anglePerRay * indexRay))
        self.visionRayLength[indexRay] = lengthRay
        self.visionRayObject[indexRay] = type

    def resetVisionRay(self,indexRay):
        anglePerRay = self.fourmiAngleOfVision / self.fourmiNbRay
        lengthRay = self.fourmiSenseRadius + self.radius
        self.visionRayCoordinate[indexRay][0] = self.coordinate[0] + lengthRay * (
            np.cos(self.angle + anglePerRay * indexRay))
        self.visionRayCoordinate[indexRay][1] = self.coordinate[1] + lengthRay * (
            np.sin(self.angle + anglePerRay * indexRay))
        self.visionRayObject[indexRay] = None
        self.visionRayLength[indexRay] = lengthRay

    def smell(self,fourmis,grasses):
        anglePerRay = self.fourmiAngleOfVision / self.fourmiNbRay
        lengthRay = self.fourmiSenseRadius + self.radius
        for indexRay in range(self.fourmiNbRay):
            L = self.visionRayCoordinate[indexRay]
            E = self.coordinate
            isColidingOnce = False
            for fourmi in fourmis:
                if fourmi != self:
                    C = fourmi.coordinate
                    if calcDistanceBetweenTwoPoint(C,E) < lengthRay:
                        r = fourmi.radius
                        isColiding = lineColideWithCircle(L,E,C,r)
                        if isColiding :
                            self.updateVisionRay(indexRay,L,E,C,r,0)
                            isColidingOnce = True
                            break
            if not isColidingOnce:
                for grass in grasses:
                    C = grass.coordinate
                    if calcDistanceBetweenTwoPoint(C, E) < lengthRay:
                        r = grass.radius
                        isColiding = lineColideWithCircle(L, E, C, r)
                        if isColiding:
                            self.updateVisionRay(indexRay,L,E,C,r,1)
                            isColidingOnce = True
                            break
            if not isColidingOnce:
                self.resetVisionRay(indexRay)





    def eat(self, foods):
        self.hasEaten = False
        for food in foods:
            if aColideWithB(self.coordinate[0], self.coordinate[1], self.radius, food.coordinate[0],
                            food.coordinate[1]) and self.hungriness > self.hungrinessThreshold:
                r = np.random.uniform()
                if r <0.5 and self.foodCarried==None and self.type != FourmiType.REINE and not self.isEgg:
                    self.foodCarried = food
                    food.carried(self.coordinate[0],self.coordinate[1])
                else:
                    if (self.foodCarried !=None and self.foodCarried != food) or self.foodCarried == None:
                        food.eaten()
                        self.hasEaten = True
                        self.health += self.bonusHealth
                        self.nbAte += 1
                        self.hungriness = 0
        if not self.hasEaten:
            self.hungriness += 1

    def act(self, grasses,deadBodies):
        food = grasses + deadBodies
        if (self.type == FourmiType.OUVRIERE) :
            self.agent.play(self, food)

    def isHatched(self):
        if self.age >= 0 and self.nbAte>=self.reproductionThreshold and self.isEgg:
            self.isEgg = False
            self.age = 0

    def dying(self):
        self.health -= 1
        self.age+=1
        if self.age >= self.death_age:
            self.die()
        self.radius = int(self.initialRadius * (self.health / self.initHealth))
        if self.radius > self.initialRadius:
            self.radius = self.initialRadius
        if self.radius < 10:
            self.radius = 10



    def die(self):
        self.health = 0
        self.isDead = True

    def shouldReproduce(self):
        if self.nbAte >= self.reproductionThreshold and self.type == FourmiType.REINE:
            self.nbAte = 0
            self.nbOffspring += 1
            return True
        return False


    def carried(self,x,y):
        self.isCarried = True
        self.coordinate = np.array([x,y])

    def eaten(self):
        self.health = 0
        self.isEaten = True
        self.isCarried = False
        self.isDead = True 

    def interaction_between_colonies(self, creatures):
        for creature in creatures:
            if aColideWithB(self.coordinate[0], self.coordinate[1], self.radius, creature.coordinate[0],
                            creature.coordinate[1]):

                # Si les fourmis qui se rencontrent ne sont pas de la même colonie, elles se battent
                if creature.colonieId != self.colonieId:
                    if self.isEgg:
                        if not self.creature.isEgg:
                            self.eaten() # L'oeuf se fait manger par la fourmi adverse
                        else:
                            continue # Si les deux fourmis sont des oeufs, rien ne se passe
                    
                    # Le degré de la blessure va dépendre de la santé des deux fourmis 
                    if creature.health > 0 and self.health > 0:
                        injury_degree = self.random.beta(creature.health, self.health)
                        self.health = int(self.health * injury_degree)



