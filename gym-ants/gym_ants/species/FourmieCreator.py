import random
import numpy as np
from copy import deepcopy
from . import SpeciesCreator
from . import Fourmi, FourmiType

class FourmieCreator(SpeciesCreator):
    """
    Classes for the creation of ours species.
    """

    def __init__(self, maxX, maxY, number, initRadius, initHealth, bonusHealthWhenEat, reproductionThreshold, hungrinessThreshold,pas, nbFourmiPerColonie, nbFourmiColonie, timeInEggForm, senseRadius, numberRay, angleOfVision):
        super().__init__(maxX, maxY, number, initRadius, initHealth, bonusHealthWhenEat, reproductionThreshold, hungrinessThreshold,pas)
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

        self.initColor()

    def create(self,parent=None) :

        if (self.firstFourmiInColonie and parent == None):
            type = FourmiType.REINE
            parent = None
        else :
            type = FourmiType.OUVRIERE
            parent = self.currentColonieReine

        fourmie = self.Create(parent, type)
        self.numberFourmiesCreatedPerColonie+=1
        self.Update()
        return fourmie

    def Update(self) :
        if (self.nbFourmiPerColonie >= self.numberFourmiesCreatedPerColonie) :
            self.firstFourmiInColonie = False
        else :
            self.firstFourmiInColonie = True
            self.numberFourmiesCreatedPerColonie = 0
            self.colonieInCreationId += 1
            self.initColor()
            self.currentColonieReine = None

    def initColor(self) :
        r = random.randint(0, 100)
        g = random.randint(0, 100)
        b = random.randint(0, 100)
        self.colonieInCreationColor = (r,g,b)

    def Create(self,parent=None,type=1):

        if parent == None:
            x = random.randint(0, self.maxX)
            y = random.randint(0, self.maxY)
            angle = random.randint(0, self.maxX)
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

            angle = random.randint(-12, 12)
            dx = np.cos(angle)
            dy = np.sin(angle)
            x = parent.coordinate[0]+(2*parent.radius)*dx
            y = parent.coordinate[1]+(2*parent.radius)*dy
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
            fourmi.agent = deepcopy(parent.agent)
        return fourmi
