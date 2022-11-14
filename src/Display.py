import pygame as pg
import numpy as np
import settings

class Display:
    def __init__(self, motionService, nbColonieFourmis):
        self.screenSizeX = settings.SCREEN_SIZE_X
        self.screenSizeY = settings.SCREEN_SIZE_Y
        self.nbHerbivore = 0
        self.nbCarnivore = 0
        self.nbFourmis = 0
        self.TYPE_REINE = 0
        self.TYPE_OUVRIERE=1
        self.nbColonieFourmis = nbColonieFourmis
        self.app = pg.display.set_mode((settings.APP_SIZE_X, settings.SCREEN_SIZE_Y))
        self.screen = pg.Surface((settings.SCREEN_SIZE_X, settings.SCREEN_SIZE_Y))
        self.font = pg.font.Font('freesansbold.ttf', 16)
        
        self.app.fill((42,48,65))
        

        self.motionService = motionService

    def displayAll(self,herbivores,carnivores,fourmis,dish, eventHandler):
        self.screen.fill((255, 255, 255))
        self.app.fill((42,48,65))
        self.display_obstacles(dish.obstacles, fourmis)
        self.displayHerbivores(herbivores)
        self.displayCarnivores(carnivores)
        self.displayFourmis(fourmis,eventHandler)
        
        self.displayDish(dish,eventHandler)
        self.displayInformation()
        self.displaySelectedCellInfo()
        self.displayInstructions(eventHandler.grassEditMode)
        self.app.blit(self.screen, (200,0))

        pg.display.flip()

    def displaySelectedCellInfo(self):
        cell = self.motionService.itemSelected
        if cell != None and self.motionService.IsFourmiSelected():
            width = 150
            height = 100
            offset = 20 + cell.radius
            leftCornerX = cell.coordinate[0]-width/2
            leftCornerY =  cell.coordinate[1]-height - offset
            leftCornerTriangleX =  cell.coordinate[0]-10
            leftCornerTriangleY = cell.coordinate[1] - offset
            rightCornerTriangleX = cell.coordinate[0] + 10
            rightCornerTriangleY = cell.coordinate[1] - offset
            bottomCornerTriangleX = cell.coordinate[0]
            bottomCornerTriangleY = cell.coordinate[1] - cell.radius

            pg.draw.rect(self.screen, pg.Color((255,255,153)), pg.Rect(leftCornerX,leftCornerY,width,height),0,border_radius=0)
            pg.draw.polygon(self.screen,pg.Color((255,255,153)),[(leftCornerTriangleX,leftCornerTriangleY),
                                                                 (rightCornerTriangleX,rightCornerTriangleY),
                                                                 (bottomCornerTriangleX,bottomCornerTriangleY)])
            health = self.font.render('Health : '+str(cell.health), True, (0, 0, 0))
            self.screen.blit(health,(leftCornerX+5,leftCornerY+5))



    def displayInformation(self):

        nbHerbivoreTxt = self.font.render('NbHerbivore : '+str(self.nbHerbivore), True,(255,255,255))
        nbCarnivoreTxt = self.font.render('NbCarnivore : ' + str(self.nbCarnivore), True, (255,255,255))
        nbFourmiTxt = self.font.render('NbFourmi : ' + str(self.nbFourmis), True, (255,255,255))
        pg.draw.rect(self.app, pg.Color((255, 255, 204)), pg.Rect(5,5,180,80),2,border_radius=5)
        self.app.blit(nbHerbivoreTxt,(10,15))
        self.app.blit(nbCarnivoreTxt, (10, 30))
        self.app.blit(nbFourmiTxt, (10, 45))

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
                    for indexRay in range(fourmi.fourmiNbRay):
                        pg.draw.line(self.screen,pg.Color((fourmi.r,fourmi.g,fourmi.b)),fourmi.coordinate,fourmi.visionRayCoordinate[indexRay])
                self.nbFourmis += 1
            else:
                pg.draw.circle(self.screen, pg.Color((fourmi.r,fourmi.g,fourmi.b)), fourmi.coordinate, fourmi.radius)


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

    def GetColonieColor(self, colonieId, fourmis) :
        for foumi in fourmis :
            if foumi.colonieId == colonieId :
                return foumi.r , foumi.g ,foumi.b
    
    def display_obstacles(self, obstacles, fourmis) :
        for obstacle in obstacles :
            obstacle.update()
            if (obstacle is not None) :
                shape = obstacle.get_shape()
                if(obstacle.isAuntHill()) :
                    
                    position = shape.center
                    color_r , color_g, color_b= self.GetColonieColor(obstacle.colonieId, fourmis)
                    pg.draw.circle(self.screen, (color_r+50 , color_g+50, color_b+50), position,100)
                
                self.screen.blit(obstacle.get_image(), shape)

                    
            


         