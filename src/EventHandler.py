import pygame as pg

class EventHandler:
    def __init__(self,grassZoneEditRadius):
        self.grassZoneEditRadius = grassZoneEditRadius
        self.grassEditMode = False

    def handleEvent(self,e,instance):
        if e.type == pg.QUIT:
            running = False
        if self.grassEditMode:
            self.handleGrassEditMode(e,instance)
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_g:
                self.toggleGrassEditMode()

    def handleGrassEditMode(self,e,instance):
        if e.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            if e.button == 1:
                instance.dish.addGrassesGrowCoordinates(pos)
            elif e.button == 3:
                instance.dish.removeGrassesGrowCoordinates(pos)


    def toggleGrassEditMode(self):
        self.grassEditMode = not self.grassEditMode