from abc import ABC, abstractmethod
from . import Species
import settings

class SpeciesCreator(ABC):
    """
    Classes for the creation of ours species.
    """

    @abstractmethod
    def __init__(self, number, initRadius, initHealth, bonusHealthWhenEat, reproductionThreshold, hungrinessThreshold,pas) :
        self.maxX = settings.SCREEN_SIZE_X
        self.maxY = settings.SCREEN_SIZE_Y
        self.number = number
        self.initRadius = initRadius
        self.initHealth = initHealth
        self.bonusHealthWhenEat = bonusHealthWhenEat
        self.reproductionThreshold = reproductionThreshold
        self.hungrinessThreshold = hungrinessThreshold
        self.pas = pas

    @abstractmethod
    def create(self,parent=None):
        pass

    def initSpecies(self) :

        species = []
        for _ in range(self.number):
            carnivore = self.create()
            species.append(carnivore)

        return species