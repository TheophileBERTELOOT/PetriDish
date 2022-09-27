import pygame as pg

class Display:
    def __init__(self,SCREEN_SIZE_X,SCREEN_SIZE_Y):
        self.screenSizeX = SCREEN_SIZE_X
        self.screenSizeY = SCREEN_SIZE_Y
        self.nbHerbivore = 0
        self.nbCarnivore = 0
        self.screen = pg.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
        self.font = pg.font.Font('freesansbold.ttf', 16)

    def displayAll(self,herbivores,carnivores,dish,eventHandler):
        self.screen.fill((255, 255, 255))
        self.displayHerbivores(herbivores)
        self.displayCarnivores(carnivores)
        self.displayDish(dish,eventHandler)
        self.displayInformation()
        self.displayInstructions(eventHandler.grassEditMode)
        pg.display.flip()

    def displayInformation(self):
        nbHerbivoreTxt = self.font.render('NbHerbivore : '+str(self.nbHerbivore), True,(0,0,0))
        nbCarnivoreTxt = self.font.render('NbCarnivore : ' + str(self.nbCarnivore), True, (0, 0, 0))
        self.screen.blit(nbHerbivoreTxt,(10,15))
        self.screen.blit(nbCarnivoreTxt, (10, 30))

    def displayInstructions(self,isGrassEditMode):
        if isGrassEditMode:
            instruction = self.font.render('Zone d\'apparition des herbes : '
                                              'Left click : add Zone / Right click : remove zone', True, (0, 0, 0))
            self.screen.blit(instruction,(self.screenSizeX/2,self.screenSizeY-30))

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

    def displayGrassesEditZones(self,dish):
        for zone in dish.shouldGrowCoordinate:
            pg.draw.circle(self.screen, pg.Color((135,243, 139)), (zone[0], zone[1]),
                           dish.grassZoneEditRadius)

    def displayDish(self,dish,eventHandler):
        self.displayGrasses(dish.grasses)
        if eventHandler.grassEditMode:
            self.displayGrassesEditZones(dish)