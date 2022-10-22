import pygame as pg
import numpy as np
from src.Display import Display
from src.Instance import Instance
from src.EventHandler import EventHandler

pg.init()
running = True
SCREEN_SIZE_X = 1600
SCREEN_SIZE_Y = 1000

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


grassRadius=5
nbGrass=20
grassZoneEditRadius=50
herbivorePas=1
carnivorePas=1
fourmiPas=1

bodyDecayingThreshold = -1000

display = Display(SCREEN_SIZE_X,SCREEN_SIZE_Y)
instance = Instance(nbHerbivore,SCREEN_SIZE_X,SCREEN_SIZE_Y,
                    herbivoreInitRadius,herbivoreInitHealth,herbivoreBonusHealthWhenEat,herbivoreReproductionThreshold,herbivoreHungrinessThreshold,
                    nbCarnivore,carnivoreInitRadius,carnivoreInitHealth,carnivoreBonusHealthWhenEat,carnivoreReproductionThreshold,carnivoreHungrinessThreshold,
                    nbFourmiPerColonie,nbFourmiColonie,fourmiInitRadius,fourmiInitHealth,fourmiBonusHealthWhenEat,fourmiReproductionThreshold,fourmiHungrinessThreshold,
                    timeInEggForm,fourmiSenseRadius,fourmiNbRay,fourmiAngleOfVision,
                    herbivorePas,carnivorePas,fourmiPas,nbGrass,grassRadius,grassZoneEditRadius,bodyDecayingThreshold)
eventHandler = EventHandler(grassZoneEditRadius)

while running:
    instance.updateDish()
    instance.cellsAct()
    instance.isGoingThroughWall()
    display.displayAll(instance.herbivores,instance.carnivores,instance.fourmis,instance.dish,eventHandler)
    for e in pg.event.get():
        eventHandler.handleEvent(e,instance)


pg.quit()