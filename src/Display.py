import pygame as pg

class Display:
    def __init__(self,SCREEN_SIZE_X,SCREEN_SIZE_Y):
        self.screenSizeX = SCREEN_SIZE_X
        self.screenSizeY = SCREEN_SIZE_Y
        self.nbHerbivore = 0
        self.nbCarnivore = 0
        self.screen = pg.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
        self.font = pg.font.Font('freesansbold.ttf', 16)

    def displayAll(self,herbivores,grasses,carnivores):
        self.screen.fill((255, 255, 255))
        self.displayHerbivores(herbivores)
        self.displayCarnivores(carnivores)
        self.displayGrasses(grasses)
        self.displayInformation()
        pg.display.flip()

    def displayInformation(self):
        nbHerbivoreTxt = self.font.render('NbHerbivore : '+str(self.nbHerbivore), True,(0,0,0))
        nbCarnivoreTxt = self.font.render('NbCarnivore : ' + str(self.nbCarnivore), True, (0, 0, 0))
        self.screen.blit(nbHerbivoreTxt,(10,15))
        self.screen.blit(nbCarnivoreTxt, (10, 30))

    def displayHerbivores(self,herbivores):
        self.nbHerbivore=0
        for herbivore in herbivores:
            if herbivore.health>0:
                pg.draw.circle(self.screen, pg.Color((herbivore.r,herbivore.g,herbivore.b)), (herbivore.x,herbivore.y), herbivore.radius)
                self.nbHerbivore+=1



    def displayCarnivores(self,carnivores):
        self.nbCarnivore=0
        for carnivore in carnivores:
            if carnivore.health>0:
                pg.draw.circle(self.screen, pg.Color((carnivore.r, 0, 0)),
                               (carnivore.x, carnivore.y), carnivore.radius+2)
                pg.draw.circle(self.screen, pg.Color((carnivore.r,carnivore.g,carnivore.b)), (carnivore.x,carnivore.y), carnivore.radius)
                self.nbCarnivore += 1

    def displayGrasses(self,grasses):
        for grass in grasses:
            pg.draw.circle(self.screen, grass.color, (grass.x,grass.y), grass.radius)