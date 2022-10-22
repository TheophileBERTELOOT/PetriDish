import pygame as pg
import numpy as np

class Display:
    def __init__(self,SCREEN_SIZE_X,SCREEN_SIZE_Y):
        self.screenSizeX = SCREEN_SIZE_X
        self.screenSizeY = SCREEN_SIZE_Y
        self.nbHerbivore = 0
        self.nbCarnivore = 0
        self.nbFourmis = 0
        self.TYPE_REINE = 0
        self.TYPE_OUVRIERE=1
        self.screen = pg.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
        self.font = pg.font.Font('freesansbold.ttf', 16)

    def displayAll(self,herbivores,carnivores,fourmis,dish,eventHandler):
        self.screen.fill((255, 255, 255))
        self.displayHerbivores(herbivores)
        self.displayCarnivores(carnivores)
        self.displayFourmis(fourmis,eventHandler)
        self.displayDish(dish,eventHandler)
        self.displayInformation()
        self.displayInstructions(eventHandler.grassEditMode)
        pg.display.flip()

    def displayInformation(self):
        nbHerbivoreTxt = self.font.render('NbHerbivore : '+str(self.nbHerbivore), True,(0,0,0))
        nbCarnivoreTxt = self.font.render('NbCarnivore : ' + str(self.nbCarnivore), True, (0, 0, 0))
        nbFourmiTxt = self.font.render('NbFourmi : ' + str(self.nbFourmis), True, (0, 0, 0))
        self.screen.blit(nbHerbivoreTxt,(10,15))
        self.screen.blit(nbCarnivoreTxt, (10, 30))
        self.screen.blit(nbFourmiTxt, (10, 45))

    def displayInstructions(self,isGrassEditMode):
        if isGrassEditMode:
            instruction = self.font.render('Zone d\'apparition des herbes : '
                                              'Left click : add Zone / Right click : remove zone', True, (0, 0, 0))
            self.screen.blit(instruction,(self.screenSizeX/2,self.screenSizeY-30))

    def displayHerbivores(self,herbivores):
        self.nbHerbivore=0
        for herbivore in herbivores:
            if herbivore.health>0:
                pg.draw.circle(self.screen, pg.Color((herbivore.r,herbivore.g,herbivore.b)), herbivore.coordinate, herbivore.radius)
                self.nbHerbivore+=1

    def displayFourmis(self,fourmis,eventHandler):
        self.nbFourmis=0
        for fourmi in fourmis:
            if fourmi.health>0:
                if fourmi.type == self.TYPE_REINE:
                    pg.draw.circle(self.screen, pg.Color((255, 255, 0)), fourmi.coordinate,
                                   fourmi.radius+3)
                if fourmi.isEgg:
                    pg.draw.circle(self.screen, pg.Color((0, 0, 0)), fourmi.coordinate,
                                   fourmi.radius/2)
                else:
                    pg.draw.circle(self.screen, pg.Color((fourmi.r,fourmi.g,fourmi.b)), fourmi.coordinate, fourmi.radius)
                if fourmi.foodCarried != None:
                    foodCarriedCoordinate = fourmi.coordinate + np.array([((fourmi.radius+2)*fourmi.dx),((fourmi.radius+2)*fourmi.dy)])
                    pg.draw.circle(self.screen,fourmi.foodCarried.color, foodCarriedCoordinate,fourmi.foodCarried.radius)

                if eventHandler.seeVisionRay:
                    anglePerRay = fourmi.fourmiAngleOfVision/fourmi.fourmiNbRay
                    for indexRay in range(fourmi.fourmiNbRay):
                        pg.draw.line(self.screen,pg.Color((fourmi.r,fourmi.g,fourmi.b)),fourmi.coordinate,fourmi.visionRayCoordinate[indexRay])

                self.nbFourmis+=1

    def displayCarnivores(self,carnivores):
        self.nbCarnivore=0
        for carnivore in carnivores:
            if carnivore.health>0:
                pg.draw.circle(self.screen, pg.Color((carnivore.r, 0, 0)),
                               carnivore.coordinate, carnivore.radius+2)
                pg.draw.circle(self.screen, pg.Color((carnivore.r,carnivore.g,carnivore.b)), carnivore.coordinate, carnivore.radius)
                self.nbCarnivore += 1

    def displayGrasses(self,grasses):
        for grass in grasses:
            if not grass.isCarried:
                pg.draw.circle(self.screen, grass.color, grass.coordinate, grass.radius)

    def displayGrassesEditZones(self,dish):
        for zone in dish.shouldGrowCoordinate:
            pg.draw.circle(self.screen, pg.Color((135,243, 139)), (zone[0], zone[1]),
                           dish.grassZoneEditRadius)

    def displayDish(self,dish,eventHandler):
        self.displayGrasses(dish.grasses)
        if eventHandler.grassEditMode:
            self.displayGrassesEditZones(dish)