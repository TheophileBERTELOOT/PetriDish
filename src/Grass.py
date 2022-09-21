import pygame as pg
import random
class Grass:
    def __init__(self,x,y,radius,maxX,maxY):
        self.x=x
        self.y=y
        self.maxX=maxX
        self.maxY=maxY
        self.radius=radius
        self.color=pg.Color(0,255,0)

    def eaten(self):
        self.x = random.randint(0,self.maxX)
        self.y = random.randint(0,self.maxY)
