import pygame as pg
import numpy as np
from src.Display import Display
from src.Instance import Instance
from src.EventHandler import EventHandler
from src.species import FourmieCreator, HerbivorCreator, CarnivoreCreator
from src.MotionService import MotionService

pg.init()
running = True

nbHerbivore = 0
herbivoreInitRadius=20
herbivoreInitHealth=10000
herbivoreBonusHealthWhenEat=10000
herbivoreReproductionThreshold=2
herbivoreHungrinessThreshold=75


nbCarnivore = 0
carnivoreInitRadius=20
carnivoreInitHealth=10000
carnivoreBonusHealthWhenEat=10000
carnivoreReproductionThreshold=3
carnivoreHungrinessThreshold=25

nbFourmiPerColonie = 5
nbFourmiColonie = 2
timeInEggForm = 500
fourmiInitRadius=20
fourmiInitHealth=10000
fourmiBonusHealthWhenEat=10000
fourmiReproductionThreshold=3
fourmiHungrinessThreshold=25
fourmiSenseRadius=150
fourmiNbRay = 10
fourmiAngleOfVision = np.pi*2

positionObstacles = [(100, 100), (200,200)]


grassRadius=5
nbGrass=20
grassZoneEditRadius=50
herbivorePas=1
carnivorePas=1
fourmiPas=1

bodyDecayingThreshold = -1000

motionService = MotionService()
display = Display(motionService, nbFourmiColonie)
herbivorCreator = HerbivorCreator(nbHerbivore, herbivoreInitRadius,herbivoreInitHealth, herbivoreBonusHealthWhenEat, herbivoreReproductionThreshold, herbivoreHungrinessThreshold, herbivorePas)
carnivorCreator = CarnivoreCreator(nbCarnivore,carnivoreInitRadius,carnivoreInitHealth,carnivoreBonusHealthWhenEat, carnivoreReproductionThreshold, carnivoreHungrinessThreshold, carnivorePas)
fourmieCreator = FourmieCreator(nbFourmiPerColonie*nbFourmiColonie,fourmiInitRadius,fourmiInitHealth,fourmiBonusHealthWhenEat,fourmiReproductionThreshold,fourmiHungrinessThreshold,fourmiPas,  nbFourmiPerColonie,nbFourmiColonie, timeInEggForm, fourmiSenseRadius, fourmiNbRay, fourmiAngleOfVision)

instance = Instance(nbGrass,grassRadius,grassZoneEditRadius,bodyDecayingThreshold, herbivorCreator, carnivorCreator, fourmieCreator, positionObstacles)

eventHandler = EventHandler(grassZoneEditRadius, motionService)


while running:
    instance.updateDish()
    instance.cellsAct()
    instance.isGoingThroughWall()
    display.displayAll(instance.herbivores,instance.carnivores,instance.fourmis,instance.dish, eventHandler)
    for e in pg.event.get():
        running = eventHandler.handleEvent(e,instance)

    pg.display.update()


pg.quit()