import numpy as np
import pygame as pg


class AntHill:

    def __init__(self, left, top,colonieId, colonieColor) :
        self.center = np.array([left,top],dtype=float)
        self.radius = 300
        self.colonieId = colonieId
        self.color = self.GetColor(colonieColor)

    def GetColor(self, colonieColor) :
        color_r = min(colonieColor.r+50 , 255)
        color_g = min(colonieColor.g+50 , 255)
        color_b = min(colonieColor.b+50 , 255)
        return pg.Color((color_r, color_b, color_g))
