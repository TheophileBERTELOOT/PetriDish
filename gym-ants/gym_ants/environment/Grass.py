import pygame as pg
import numpy as np
import random
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
        self.isEaten = False
        self.isCarried = False
        r = random.random()
        if r > 0.5:
            r = random.random()
            self.coordinate[0] = random.randint(0, self.maxX)
            if r > 0.5:
                self.coordinate[1] = random.randint(0, 100)
            else:
                self.coordinate[1] = random.randint(self.maxY - 100, self.maxY)
        else:
            r = random.random()
            self.coordinate[1] = random.randint(0, self.maxY)
            if r > 0.5:
                self.coordinate[0] = random.randint(0, 100)
            else:
                self.coordinate[0] = random.randint(self.maxX - 100, self.maxX)

    def carried(self,x,y):
        self.isCarried = True
        self.coordinate = np.array([x,y])
