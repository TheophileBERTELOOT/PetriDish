import numpy as np
from src.util import calcDistanceBetweenTwoPoint
from src.species import Fourmi 
from src.Obstacle import Obstacle 
import settings

MOVESPEED = 6

class MotionService:

    def __init__(self):
        self.itemSelected = None
    
    def SelectItem(self, position, instance) :
        arrayPos = np.array(position)
        arrayPos[0] -= settings.APP_SIZE_X - settings.SCREEN_SIZE_X
        noCellSelected = True
        for obstacle in instance.dish.obstacles:
            if obstacle.get_shape().collidepoint(arrayPos[0], arrayPos[1]):
                self.itemSelected  = obstacle
                noCellSelected = False
                break
        for fourmi in instance.fourmis:
            if calcDistanceBetweenTwoPoint(fourmi.coordinate,arrayPos)<fourmi.radius:
                self.itemSelected  = fourmi
                noCellSelected = False
                break
        if (noCellSelected) :
            self.itemSelected = None

    def IsFourmiSelected(self):
        return isinstance(self.itemSelected, Fourmi)

    def MoveObstacle(self, moveUp, moveDown, moveLeft, moveRight ) :
        if (isinstance(self.itemSelected, Obstacle)) :
            shape = self.itemSelected.get_shape()
            if moveDown and shape.bottom < settings.SCREEN_SIZE_Y:
                shape.top += MOVESPEED
            if moveUp and shape.top > 0:
                shape.top -= MOVESPEED
            if moveLeft and shape.left > 0:
                shape.left -= MOVESPEED
            if moveRight and shape.right < settings.SCREEN_SIZE_X:
                shape.right += MOVESPEED
        
        
    