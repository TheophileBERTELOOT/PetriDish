import pygame as pg

from src.Display import Display
from src.Instance import Instance

pg.init()
running = True
SCREEN_SIZE_X = 1600
SCREEN_SIZE_Y = 1000
nbHerbivore = 50
herbivoreInitRadius=20
grassRadius=5
nbGrass=20
pas=1

display = Display(SCREEN_SIZE_X,SCREEN_SIZE_Y)
instance = Instance(nbHerbivore,SCREEN_SIZE_X,SCREEN_SIZE_Y,herbivoreInitRadius,pas,nbGrass,grassRadius)

while running:
    instance.herbivoresRun()
    instance.herbivoresAct()
    instance.isGoingThroughWall()
    display.displayAll(instance.herbivores,instance.grasses)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        if e.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()

pg.quit()