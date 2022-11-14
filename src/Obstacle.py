import numpy as np
import pygame as pg


class Obstacle:

    def __init__(self, left, top, width, height, image='pebble.png') :
        self._pebble = pg.image.load(image)
        self.shape = pg.Rect(left, top, width, height)
        self._pebbleStretchedImage = pg.transform.scale(self._pebble, (self.shape.width, self.shape.height))
        self.coordinate = np.array([left,top],dtype=float)
        self.colonieId = None

    def update(self):
        self._pebbleStretchedImage = pg.transform.scale(self._pebble, (self.shape.width, self.shape.height))

    def get_image(self):
        return self._pebbleStretchedImage

    def get_shape(self) :
        return self.shape

    def isAuntHill(self): 
        return self.colonieId is not None
    
    def tryGetColonized(self, colonieId) :
        if (self.colonieId is None) :
            self.colonieId = colonieId

    