import pygame as pg
import numpy as np

class Grass:
    def __init__(self,x,y,radius,maxX,maxY):
        self.coordinate = np.array([x,y])
        self.maxX=maxX
        self.maxY=maxY
        self.radius=radius
        self.isEaten = False
        self.isCarried = False
        self.color=pg.Color(0,255,0)

    def eaten(self):
        self.isEaten = True
        self.isCarried = False

    def carried(self,x,y):
        self.isCarried = True
        self.coordinate = np.array([x,y])
