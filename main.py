import pygame as pg
import numpy as np
from src.Display import Display
from src.Instance import Instance
from src.EventHandler import EventHandler
from src.species import FourmieCreator, HerbivorCreator, CarnivoreCreator

pg.init()
running = True
SCREEN_SIZE_X = 500
SCREEN_SIZE_Y = 500

nbHerbivore = 3
herbivoreInitRadius=20
herbivoreInitHealth=10000
herbivoreBonusHealthWhenEat=10000
herbivoreReproductionThreshold=2
herbivoreHungrinessThreshold=75


nbCarnivore = 5
carnivoreInitRadius=20
carnivoreInitHealth=10000
carnivoreBonusHealthWhenEat=10000
carnivoreReproductionThreshold=3
carnivoreHungrinessThreshold=25

nbFourmiPerColonie = 2
nbFourmiColonie = 1
timeInEggForm = 500
fourmiInitRadius=20
fourmiInitHealth=10000
fourmiBonusHealthWhenEat=10000
fourmiReproductionThreshold=3
fourmiHungrinessThreshold=25
fourmiSenseRadius=150
fourmiNbRay = 10
fourmiAngleOfVision = np.pi*2

positionObstacle = (100, 100)


grassRadius=5
nbGrass=20
grassZoneEditRadius=50
herbivorePas=1
carnivorePas=1
fourmiPas=1

bodyDecayingThreshold = -1000

display = Display(SCREEN_SIZE_X,SCREEN_SIZE_Y)
herbivorCreator = HerbivorCreator(SCREEN_SIZE_X, SCREEN_SIZE_Y, nbHerbivore, herbivoreInitRadius,herbivoreInitHealth, herbivoreBonusHealthWhenEat, herbivoreReproductionThreshold, herbivoreHungrinessThreshold, herbivorePas)
carnivorCreator = CarnivoreCreator(SCREEN_SIZE_X, SCREEN_SIZE_Y, nbCarnivore,carnivoreInitRadius,carnivoreInitHealth,carnivoreBonusHealthWhenEat, carnivoreReproductionThreshold, carnivoreHungrinessThreshold, carnivorePas)
fourmieCreator = FourmieCreator(SCREEN_SIZE_X, SCREEN_SIZE_Y, nbFourmiPerColonie*nbFourmiColonie,fourmiInitRadius,fourmiInitHealth,fourmiBonusHealthWhenEat,fourmiReproductionThreshold,fourmiHungrinessThreshold,fourmiPas,  nbFourmiPerColonie,nbFourmiColonie, timeInEggForm, fourmiSenseRadius, fourmiNbRay, fourmiAngleOfVision)

instance = Instance(SCREEN_SIZE_X, SCREEN_SIZE_Y,nbGrass,grassRadius,grassZoneEditRadius,bodyDecayingThreshold, herbivorCreator, carnivorCreator, fourmieCreator, positionObstacle)
eventHandler = EventHandler(grassZoneEditRadius)

while running:
    instance.updateDish()
    instance.cellsAct()
    instance.isGoingThroughWall()
    display.displayAll(instance.herbivores,instance.carnivores,instance.fourmis,instance.dish, eventHandler)
    for e in pg.event.get():
        running = eventHandler.handleEvent(e,instance)


pg.quit()