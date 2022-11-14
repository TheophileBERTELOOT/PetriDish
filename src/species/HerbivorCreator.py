from . import SpeciesCreator
from . import Herbivore
import random
import numpy as np
from copy import deepcopy

class HerbivorCreator(SpeciesCreator):

    def __init__(self, maxX, maxY, number, initRadius, initHealth, bonusHealthWhenEat, reproductionThreshold, hungrinessThreshold,pas):
         super().__init__(maxX, maxY, number, initRadius, initHealth, bonusHealthWhenEat, reproductionThreshold, hungrinessThreshold,pas)

    def create(self,parent=None):
        if parent == None:
            x = random.randint(0, self.maxX)
            y = random.randint(0, self.maxY)
            angle = random.randint(-self.maxX, self.maxX)
            dx = np.cos(angle)
            dy = np.sin(angle)
            r = random.randint(0, 255)
            g = 255
            b = random.randint(0, 255)
            radius = self.initRadius
            health = self.initHealth
            bonusHealth = self.bonusHealthWhenEat
            reproductionThreshold = self.reproductionThreshold
            hungrinessThreshold = self.hungrinessThreshold
            pas = self.pas
            herbivore = Herbivore(x, y, dx, dy, r, g, b, radius, health, bonusHealth, reproductionThreshold,hungrinessThreshold, pas)
        else:
            x = parent.coordinate[0]
            y = parent.coordinate[1]
            angle = random.randint(-self.maxX, self.maxX)
            dx = np.cos(angle)
            dy = np.sin(angle)
            r = parent.r
            g = 255
            b = parent.b
            radius = self.initRadius
            health = self.initHealth
            bonusHealth = self.bonusHealthWhenEat
            reproductionThreshold = self.reproductionThreshold
            pas = self.pas
            hungrinessThreshold = self.hungrinessThreshold
            herbivore = Herbivore(x, y, dx, dy, r, g, b, radius, health, bonusHealth, reproductionThreshold,hungrinessThreshold, pas)
            herbivore.agent = deepcopy(parent.agent)
        return herbivore