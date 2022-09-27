import pygame as pg

from src.Display import Display
from src.Instance import Instance
from src.EventHandler import EventHandler

pg.init()
running = True
SCREEN_SIZE_X = 1600
SCREEN_SIZE_Y = 1000

nbHerbivore = 50
herbivoreInitRadius=20
herbivoreInitHealth=10000
herbivoreBonusHealthWhenEat=10000
herbivoreReproductionThreshold=2
herbivoreHungrinessThreshold=75

nbCarnivore = 10
carnivoreInitRadius=20
carnivoreInitHealth=10000
carnivoreBonusHealthWhenEat=10000
carnivoreReproductionThreshold=3
carnivoreHungrinessThreshold=25

grassRadius=5
nbGrass=40
grassZoneEditRadius=50
herbivorePas=1
carnivorePas=1

display = Display(SCREEN_SIZE_X,SCREEN_SIZE_Y)
instance = Instance(nbHerbivore,SCREEN_SIZE_X,SCREEN_SIZE_Y,
                    herbivoreInitRadius,herbivoreInitHealth,herbivoreBonusHealthWhenEat,herbivoreReproductionThreshold,herbivoreHungrinessThreshold,
                    nbCarnivore,carnivoreInitRadius,carnivoreInitHealth,carnivoreBonusHealthWhenEat,carnivoreReproductionThreshold,carnivoreHungrinessThreshold,
                    herbivorePas,carnivorePas,nbGrass,grassRadius,grassZoneEditRadius)
eventHandler = EventHandler(grassZoneEditRadius)

while running:
    instance.updateDish()
    instance.cellsAct()
    instance.isGoingThroughWall()
    display.displayAll(instance.herbivores,instance.carnivores,instance.dish,eventHandler)
    for e in pg.event.get():
        eventHandler.handleEvent(e,instance)


pg.quit()