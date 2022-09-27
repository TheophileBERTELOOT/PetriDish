import pygame as pg
import random
class Grass:
    def __init__(self,x,y,radius,maxX,maxY):
        self.x=x
        self.y=y
        self.maxX=maxX
        self.maxY=maxY
        self.radius=radius
        self.isEaten = False
        self.color=pg.Color(0,255,0)

    def eaten(self):
        self.isEaten = True
