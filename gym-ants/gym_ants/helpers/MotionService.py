import numpy as np
from src.util import calcDistanceBetweenTwoPoint
from gym_ants.species.Fourmi import Fourmi
from gym_ants.environment.Obstacle import Obstacle

MOVESPEED = 6

class MotionService:

    def __init__(self, screen_size_x, screen_size_y):
        self.itemSelected = None
        self.screen_size_x = screen_size_x
        self.screen_size_y = screen_size_y
    
    def SelectItem(self, position, instance) :
        arrayPos = np.array(position)
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
            if moveDown and shape.bottom < self.screen_size_y:
                shape.top += MOVESPEED
            if moveUp and shape.top > 0:
                shape.top -= MOVESPEED
            if moveLeft and shape.left > 0:
                shape.left -= MOVESPEED
            if moveRight and shape.right < self.screen_size_x:
                shape.right += MOVESPEED
        
        
    