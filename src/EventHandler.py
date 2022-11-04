import pygame as pg
import numpy as np
from src.util import calcDistanceBetweenTwoPoint
class EventHandler:
    def __init__(self,grassZoneEditRadius):
        self.grassZoneEditRadius = grassZoneEditRadius
        self.grassEditMode = False
        self.seeVisionRay =  False
        self.selectedCell = None


    def handleEvent(self,e,instance):
        running = True
        if e.type == pg.QUIT:
            running = False
        if self.grassEditMode:
            self.handleGrassEditMode(e,instance)
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_g:
                self.toggleGrassEditMode()
            if e.key == pg.K_v:
                self.toggleSeeVisionRay()
        if e.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            if e.button == 1:
                self.selectACell(instance,pos)

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
        arrayPos = np.array(pos)
        NoCellSelected = True
        for fourmi in instance.fourmis:
            if calcDistanceBetweenTwoPoint(fourmi.coordinate,arrayPos)<fourmi.radius:
                self.selectedCell = fourmi
                NoCellSelected = False
                break
        if NoCellSelected :
            self.selectedCell = None