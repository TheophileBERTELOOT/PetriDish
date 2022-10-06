import pygame as pg

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

nbFourmiPerColonie = 10
nbFourmiColonie = 2
fourmiInitRadius=20
fourmiInitHealth=100000
fourmiBonusHealthWhenEat=10000
fourmiReproductionThreshold=3
fourmiHungrinessThreshold=25

grassRadius=5
nbGrass=40
grassZoneEditRadius=50
herbivorePas=1
carnivorePas=1
fourmiPas=1

display = Display(SCREEN_SIZE_X,SCREEN_SIZE_Y)
instance = Instance(nbHerbivore,SCREEN_SIZE_X,SCREEN_SIZE_Y,
                    herbivoreInitRadius,herbivoreInitHealth,herbivoreBonusHealthWhenEat,herbivoreReproductionThreshold,herbivoreHungrinessThreshold,
                    nbCarnivore,carnivoreInitRadius,carnivoreInitHealth,carnivoreBonusHealthWhenEat,carnivoreReproductionThreshold,carnivoreHungrinessThreshold,
                    nbFourmiPerColonie,nbFourmiColonie,fourmiInitRadius,fourmiInitHealth,fourmiBonusHealthWhenEat,fourmiReproductionThreshold,fourmiHungrinessThreshold,
                    herbivorePas,carnivorePas,fourmiPas,nbGrass,grassRadius,grassZoneEditRadius)
eventHandler = EventHandler(grassZoneEditRadius)

while running:
    instance.updateDish()
    instance.cellsAct()
    instance.isGoingThroughWall()
    display.displayAll(instance.herbivores,instance.carnivores,instance.fourmis,instance.dish,eventHandler)
    for e in pg.event.get():
        eventHandler.handleEvent(e,instance)


pg.quit()