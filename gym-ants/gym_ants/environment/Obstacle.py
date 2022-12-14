import numpy as np
import pygame as pg


class Obstacle:

    def __init__(self, left, top, width, height, with_image, image='pebble.png') :
        if with_image :
            self.init_with_image(left, top, width, height, image)
        else :            
            self.inti_without_image(left, top, width, height)

    def inti_without_image(self, left, top, width, height) :
        self._pebble = None
        self.shape = pg.Rect(left, top, width, height)
        self._pebbleStretchedImage = None
        self.shape.width = width 
        self.shape.height = height
        self.shape.centerx = left
        self.shape.centery = top
        
        self.coordinate = np.array([left,top],dtype=float)
        self.colonieId = None
    
    def init_with_image(self, left, top, width, height, image='pebble.png') :
        self._pebble = pg.image.load(image)
        self._pebbleStretchedImage = pg.transform.scale(self._pebble, (width, height))
        self.shape = self._pebble.get_rect()
        self.shape.width = width 
        self.shape.height = height
        self.shape.centerx = left
        self.shape.centery = top
        
        self.coordinate = np.array([left,top],dtype=float)
        self.colonieId = None
    
    def update(self):
        if self.has_image():
            self._pebbleStretchedImage = pg.transform.scale(self._pebble, (self.shape.width, self.shape.height))

    def has_image(self) :
        return self._pebbleStretchedImage is not None

    def get_image(self):
        return self._pebbleStretchedImage

    def get_shape(self) :
        return self.shape

    def isAuntHill(self): 
        return self.colonieId is not None

    
    def tryGetColonized(self, colonieId) :
        if (self.colonieId is None) :
            self.colonieId = colonieId