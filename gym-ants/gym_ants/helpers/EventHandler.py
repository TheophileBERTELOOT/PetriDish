import pygame as pg
import numpy as np
from gym_ants.helpers.util import calcDistanceBetweenTwoPoint

class EventHandler:
    def __init__(self,grassZoneEditRadius , motionService):
        self.grassZoneEditRadius = grassZoneEditRadius
        self.grassEditMode = False
        self.seeVisionRay =  False
        self.motionService = motionService
        self.moveUp, self.moveDown, self.moveLeft, self.moveRight = False,False,False,False


    def handleEvent(self,event,instance):
        running = True
        if event.type == pg.QUIT:
            running = False
        if self.grassEditMode:
            self.handleGrassEditMode(event,instance)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_g:
                self.toggleGrassEditMode()
            if event.key == pg.K_v:
                self.toggleSeeVisionRay()
        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            if event.button == 1:
                self.selectACell(instance,pos)

        if event.type == pg.KEYDOWN:
            # Change the keyboard variables.
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                self.moveRight = False
                self.moveLeft = True
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                self.moveLeft = False
                self.moveRight = True
            if event.key == pg.K_UP or event.key == pg.K_w:
                self.moveDown = False
                self.moveUp = True
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                self.moveUp = False
                self.moveDown = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                self.moveLeft = False
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                self.moveRight = False
            if event.key == pg.K_UP or event.key == pg.K_w:
                self.moveUp = False
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                self.moveDown = False
        self.motionService.MoveObstacle(self.moveUp, self.moveDown, self.moveLeft, self.moveRight)

        return running


    def toggleSeeVisionRay(self):
        self.seeVisionRay = not self.seeVisionRay

    def handleGrassEditMode(self,e,instance):
        if e.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            if e.button == 1:
                instance.dish.addGrassesGrowCoordinates(pos)
            elif e.button == 3:
                instance.dish.removeGrassesGrowCoordinates(pos)

    def toggleGrassEditMode(self):
        self.grassEditMode = not self.grassEditMode

    def selectACell(self,instance,pos):
        self.motionService.SelectItem(pos, instance)