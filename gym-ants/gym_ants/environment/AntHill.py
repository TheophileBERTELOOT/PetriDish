import numpy as np
import pygame as pg


class AntHill:

    def __init__(self, queen) :
        self.queen = queen
        self.center = np.array([queen.coordinate[0],queen.coordinate[1]],dtype=float)
        self.radius = 100
        self.colonieId = queen.colonieId
        self.color = self.GetColor(queen.color)

    def GetColor(self, colonieColor) :
        color_r = min(colonieColor.r+50 , 255)
        color_g = min(colonieColor.g+50 , 255)
        color_b = min(colonieColor.b+50 , 255)
        return pg.Color((color_r, color_b, color_g))
