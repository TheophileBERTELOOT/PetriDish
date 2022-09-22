import pygame as pg

from src.Display import Display
from src.Instance import Instance

pg.init()
running = True
SCREEN_SIZE_X = 1600
SCREEN_SIZE_Y = 1000
nbHerbivore = 50
herbivoreInitRadius=20
herbivoreInitHealth=10000
herbivoreBonusHealthWhenEat=10000
herbivoreReproductionThreshold=3
nbCarnivore = 5
carnivoreInitRadius=20
carnivoreInitHealth=10000
carnivoreBonusHealthWhenEat=10000
carnivoreReproductionThreshold=3
grassRadius=5
nbGrass=30
herbivorePas=1
carnivorePas=1

display = Display(SCREEN_SIZE_X,SCREEN_SIZE_Y)
instance = Instance(nbHerbivore,SCREEN_SIZE_X,SCREEN_SIZE_Y,
                    herbivoreInitRadius,herbivoreInitHealth,herbivoreBonusHealthWhenEat,herbivoreReproductionThreshold,
                    nbCarnivore,carnivoreInitRadius,carnivoreInitHealth,carnivoreBonusHealthWhenEat,carnivoreReproductionThreshold,
                    herbivorePas,carnivorePas,nbGrass,grassRadius,)

while running:
    instance.cellsAct()
    instance.isGoingThroughWall()
    display.displayAll(instance.herbivores,instance.grasses,instance.carnivores)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        if e.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()

pg.quit()