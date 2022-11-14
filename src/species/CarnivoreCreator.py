import random
import numpy as np
from copy import deepcopy
from . import SpeciesCreator
from . import Carnivore

class CarnivoreCreator(SpeciesCreator):
    """
    Classes for the creation of ours species.
    """

    def __init__(self, maxX, maxY, number, initRadius, initHealth, bonusHealthWhenEat, reproductionThreshold, hungrinessThreshold,pas):
         super().__init__(maxX, maxY, number, initRadius, initHealth, bonusHealthWhenEat, reproductionThreshold, hungrinessThreshold,pas)
    
    def create(self, parent=None):
        if parent == None:
            x = random.randint(0, self.maxX)
            y = random.randint(0, self.maxY)
            angle = random.randint(0, self.maxX)
            dx = np.cos(angle)
            dy = np.sin(angle)
            r = 255
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            radius = self.initRadius
            health = self.initHealth
            bonusHealth = self.bonusHealthWhenEat
            reproductionThreshold = self.reproductionThreshold
            hungrinessThreshold = self.hungrinessThreshold
            pas = self.pas
            carnivore = Carnivore(x, y, dx, dy, r, g, b, radius, health, bonusHealth, reproductionThreshold,hungrinessThreshold, pas)
        else:
            x = parent.coordinate[0]
            y = parent.coordinate[1]
            angle = random.randint(0, self.maxX)
            dx = np.cos(angle)
            dy = np.sin(angle)
            r = 255
            g = parent.g
            b = parent.b
            radius = self.initRadius
            health = self.initHealth
            bonusHealth = self.bonusHealthWhenEat
            reproductionThreshold = self.reproductionThreshold
            hungrinessThreshold = self.hungrinessThreshold
            pas = self.pas
            carnivore = Carnivore(x, y, dx, dy, r, g, b, radius, health, bonusHealth, reproductionThreshold,hungrinessThreshold, pas)
            carnivore.agent = deepcopy(parent.agent)
        return carnivore
