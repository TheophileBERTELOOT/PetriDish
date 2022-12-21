import random
import numpy as np
from copy import deepcopy
from . import SpeciesCreator
from . import Fourmi, FourmiType

class FourmieCreator(SpeciesCreator):
    """
    Classes for the creation of ours species.
    """

    def __init__(self, maxX, maxY, number, initRadius, initHealth, bonusHealthWhenEat, reproductionThreshold, hungrinessThreshold,pas, nbFourmiPerColonie, nbFourmiColonie, timeInEggForm, senseRadius, numberRay, angleOfVision, seed=None):
        super().__init__(maxX, maxY, number, initRadius, initHealth, bonusHealthWhenEat, reproductionThreshold, hungrinessThreshold,pas, seed)
        self.colonieInCreationId = 0
        self.firstFourmiInColonie = True
        self.numberFourmiesCreatedPerColonie = 0
        self.currentColonieReine = None
        self.nbFourmiPerColonie = nbFourmiPerColonie
        self.nbFourmiColonie = nbFourmiColonie
        self.timeInEggForm = timeInEggForm
        self.senseRadius = senseRadius 
        self.numberRay = numberRay
        self.angleOfVision = angleOfVision
        random.seed(seed)
        np.random.seed(seed)

        self.initColor()

    def create(self,parent=None) :

        if (self.firstFourmiInColonie and parent == None):
            type = FourmiType.OUVRIERE
            parent = None
        else :
            type = FourmiType.OUVRIERE
            parent = self.currentColonieReine

        fourmie = self.Create(parent, type)
        self.numberFourmiesCreatedPerColonie+=1
        self.Update()
        return fourmie

    def Update(self) :
        if (self.nbFourmiPerColonie > self.numberFourmiesCreatedPerColonie) :
            self.firstFourmiInColonie = False
        else :
            self.firstFourmiInColonie = True
            self.numberFourmiesCreatedPerColonie = 0
            self.colonieInCreationId += 1
            self.initColor()
            self.currentColonieReine = None

    def initColor(self) :
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.colonieInCreationColor = (r,g,b)

    def Create(self,parent=None,type=1):

        if parent == None:
            x = self.maxX/2 + random.randint(-100,100)
            y = self.maxY/2+ random.randint(-100,100)
            angle = self.maxX
            dx = np.cos(angle)
            dy = np.sin(angle)
            radius = self.initRadius
            health = self.initHealth
            bonusHealth = self.bonusHealthWhenEat
            reproductionThreshold = self.reproductionThreshold
            hungrinessThreshold = self.hungrinessThreshold
            timeInEggForm = self.timeInEggForm
            fourmiSenseRadius = self.senseRadius
            pas = self.pas
            fourmiNbRay = self.numberRay
            fourmiAngleOfVision = self.angleOfVision
            fourmi = Fourmi(x, y, dx, dy, self.colonieInCreationColor[0],self.colonieInCreationColor[1],self.colonieInCreationColor[2], radius, health, bonusHealth, reproductionThreshold,hungrinessThreshold,
                            pas,timeInEggForm,fourmiSenseRadius,fourmiNbRay,fourmiAngleOfVision,type,self.colonieInCreationId)
            
            self.currentColonieReine = fourmi

        else:

            angle = 12
            dx = np.cos(angle)
            dy = np.sin(angle)
            x = self.maxX -300+ random.randint(-100,100)
            y = self.maxY -300+ random.randint(-100,100)
            r = parent.r
            g = parent.g
            b = parent.b
            radius = self.initRadius
            health = self.initHealth
            bonusHealth = self.bonusHealthWhenEat
            reproductionThreshold = self.reproductionThreshold
            pas = self.pas
            hungrinessThreshold = self.hungrinessThreshold
            colonieId= parent.colonieId
            timeInEggForm = self.timeInEggForm
            fourmiSenseRadius = self.senseRadius
            fourmiNbRay=self.numberRay
            fourmiAngleOfVision = self.angleOfVision
            fourmi = Fourmi(x, y, dx, dy, r, g, b, radius, health, bonusHealth, reproductionThreshold,hungrinessThreshold,
                            pas,timeInEggForm,fourmiSenseRadius,fourmiNbRay,fourmiAngleOfVision,type,colonieId)
            fourmi.normalize()
            #fourmi.agent = deepcopy(parent.agent)
        return fourmi
