import pygame as pg
import random
from gym_ants.environment.Grass import Grass
from gym_ants.environment.Obstacle import Obstacle
class Dish:
    def __init__(self,maxX,maxY,nbGrass,grassRadius,grassZoneEditRadius, positionObstacle):
        self.maxX=maxX
        self.maxY=maxY
        self.grassRadius=grassRadius
        self.nbGrass=nbGrass
        self.grasses = []
        self.shouldGrowCoordinate=[]
        self.grassZoneEditRadius = grassZoneEditRadius
        self.obstacles = []
        self.initGrasses()
        self.init_obstacles(positionObstacle)

    def addGrassesGrowCoordinates(self,co):
        self.shouldGrowCoordinate.append(co)

    def removeGrassesGrowCoordinates(self,co):
        for i in range(len(self.shouldGrowCoordinate)):
            growZone = self.shouldGrowCoordinate[i]
            isInside = co[0]<growZone[0]+self.grassZoneEditRadius and co[0]>growZone[0]-self.grassZoneEditRadius and \
            co[1] < growZone[1] + self.grassZoneEditRadius and co[1] > growZone[1] - self.grassZoneEditRadius
            if isInside:
                self.shouldGrowCoordinate.pop(i)
                break

    def initGrasses(self):
        for _ in range(self.nbGrass):
            x = random.randint(0, self.maxX)
            y = random.randint(0, self.maxY)
            radius= self.grassRadius
            grass = Grass(x,y,radius,self.maxX,self.maxY)
            self.grasses.append(grass)

    def init_obstacles(self, positionObstacle) :
        x, y = positionObstacle
        self.obstacles.append(Obstacle(x,y, 40,40))

    def regrowEatenGrasses(self):
        for grass in self.grasses:
            if grass.isEaten:
                grass.isEaten = False
                if self.shouldGrowCoordinate != []:
                    selectedZone = random.choice(self.shouldGrowCoordinate)
                    grass.coordinate[0] = random.randint(selectedZone[0]-self.grassZoneEditRadius,selectedZone[0]+self.grassZoneEditRadius)
                    grass.coordinate[1] = random.randint(selectedZone[1] - self.grassZoneEditRadius,selectedZone[1] + self.grassZoneEditRadius)
                else:
                    grass.coordinate[0] = random.randint(0,self.maxX)
                    grass.coordinate[1] = random.randint(0, self.maxY)

    def isGoingThroughWall(self,cells):
        for cell in cells:
            if cell.coordinate[0]<0:
                cell.coordinate[0] = self.maxX
            if cell.coordinate[0]>self.maxX:
                cell.coordinate[0] = 0
            if cell.coordinate[1]<0:
                cell.coordinate[1]=self.maxY
            if cell.coordinate[1]>self.maxY:
                cell.coordinate[1]=0

    def isGoingThroughObstacles(self,cell):
        for obstacle in self.obstacles :
            isCollide = obstacle.shape.collidepoint(cell.coordinate[0], cell.coordinate[1])
            if isCollide : return True
        return False
