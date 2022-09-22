import pygame as pg

class Display:
    def __init__(self,SCREEN_SIZE_X,SCREEN_SIZE_Y):
        self.screenSizeX = SCREEN_SIZE_X
        self.screenSizeY = SCREEN_SIZE_Y
        self.screen = pg.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))

    def displayAll(self,herbivores,grasses):
        self.screen.fill((255, 255, 255))
        self.displayHerbivores(herbivores)
        self.displayGrasses(grasses)
        pg.display.flip()

    def displayHerbivores(self,herbivores):
        for herbivore in herbivores:
            if herbivore.health>0:
                pg.draw.circle(self.screen, pg.Color((herbivore.r,herbivore.g,herbivore.b)), (herbivore.x,herbivore.y), herbivore.radius)

    def displayGrasses(self,grasses):
        for grass in grasses:
            pg.draw.circle(self.screen, grass.color, (grass.x,grass.y), grass.radius)