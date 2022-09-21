import pygame as pg

class Dish:
    def __init__(self,maxX,maxY):
        self.maxX=maxX
        self.maxY=maxY

    def isGoingThroughWall(self,cells):
        for cell in cells:
            if cell.x<0:
                cell.x = self.maxX
            if cell.x>self.maxX:
                cell.x = 0
            if cell.y<0:
                cell.y=self.maxY
            if cell.y>self.maxY:
                cell.y=0