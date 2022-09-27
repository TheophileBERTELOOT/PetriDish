import pygame as pg
import random
from src.Grass import Grass
class Dish:
    def __init__(self,maxX,maxY,nbGrass,grassRadius,grassZoneEditRadius):
        self.maxX=maxX
        self.maxY=maxY
        self.grassRadius=grassRadius
        self.nbGrass=nbGrass
        self.grasses = []
        self.shouldGrowCoordinate=[]
        self.grassZoneEditRadius = grassZoneEditRadius
        self.initGrasses()

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

    def regrowEatenGrasses(self):
        for grass in self.grasses:
            if grass.isEaten:
                grass.isEaten = False
                if self.shouldGrowCoordinate != []:
                    selectedZone = random.choice(self.shouldGrowCoordinate)
                    grass.x = random.randint(selectedZone[0]-self.grassZoneEditRadius,selectedZone[0]+self.grassZoneEditRadius)
                    grass.y = random.randint(selectedZone[1] - self.grassZoneEditRadius,selectedZone[1] + self.grassZoneEditRadius)
                else:
                    grass.x = random.randint(0,self.maxX)
                    grass.y = random.randint(0, self.maxY)

    def isGoingThroughWall(self,cells):
        for cell in cells:
            if cell.x<0:
                cell.x = self.maxX
            if cell.x>self.maxX:
                cell.x = 0
            if cell.y<0:
                cell.y=self.maxY
            if cell.y>self.maxY:
                cell.y=0