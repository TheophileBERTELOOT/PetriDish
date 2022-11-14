import pygame as pg
import numpy as np
from src.MotionService import MotionService
class EventHandler:
    def __init__(self,grassZoneEditRadius, motionService):
        self.grassZoneEditRadius = grassZoneEditRadius
        self.grassEditMode = False
        self.seeVisionRay =  False
        self.motionService = motionService


    def handleEvent(self,event,instance):
        running = True
        moveUp, moveDown, moveLeft, moveRight = False,False,False,False
        if event.type == pg.QUIT:
            running = False
        if self.grassEditMode:
            self.handleGrassEditMode(e,instance)
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
                moveRight = False
                moveLeft = True
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                moveLeft = False
                moveRight = True
            if event.key == pg.K_UP or event.key == pg.K_w:
                moveDown = False
                moveUp = True
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                moveUp = False
                moveDown = True
        self.motionService.MoveObstacle(moveUp, moveDown, moveLeft, moveRight)
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