from abc import ABC, abstractmethod
import numpy as np
from src.util import calcAngle

class Species(ABC):
    """
    The species interface 
    must implement.
    """
    
    @abstractmethod
    def __init__(self,x,y,dx,dy,r,g,b,radius,initHealth,bonusHealth,reproductionThreshold,hungrinessThreshold,pas, seed):
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
        self.nbOffspring = 0
        self.nbAte = 0
        self.hasEaten = False
        self.seed = seed

        self.angle = calcAngle(dx,dy)

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def deviate_obstacles(self) :
        pass

    @abstractmethod
    def normalize(self):
        pass

    @abstractmethod
    def eat(self,herbivores):
        pass

    

    @abstractmethod
    def dying(self):
        pass

    @abstractmethod
    def shouldReproduce(self,carnivores):
        pass