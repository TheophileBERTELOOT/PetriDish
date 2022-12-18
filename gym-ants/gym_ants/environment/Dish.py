import pygame as pg
import random
from gym_ants.environment.Grass import Grass
from gym_ants.environment.Obstacle import Obstacle
from gym_ants.environment.AntHill import AntHill
class Dish:
    def __init__(self,maxX,maxY,nbGrass,grassRadius,grassZoneEditRadius, positionsObstacle, antQueens):
        self.maxX=maxX
        self.maxY=maxY
        self.grassRadius=grassRadius
        self.nbGrass=nbGrass
        self.grasses = []
        self.shouldGrowCoordinate=[]
        self.grassZoneEditRadius = grassZoneEditRadius
        self.obstacles = []
        self.antHills = []
        self.initGrasses()
        self.add_obstacles(positionsObstacle)
        self.init_antHills(antQueens)

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

    def addObstaclesCoordinates(self,co):
        self.add_obstacle(co, False)

    def removeObstaclesCoordinates(self, obstacle):
        self.obstacles.remove(obstacle)

    def initGrasses(self):
        for _ in range(self.nbGrass):
            r = random.random()
            if r > 0.5:
                r = random.random()
                x = random.randint(0, self.maxX)
                if r > 0.5:
                    y = random.randint(0, 100)
                else:
                    y = random.randint(self.maxY - 100, self.maxY)
            else:
                r = random.random()
                y = random.randint(0, self.maxY)
                if r > 0.5:
                    x = random.randint(0, 100)
                else:
                    x = random.randint(self.maxX - 100, self.maxX)
            radius= self.grassRadius
            grass = Grass(x,y,radius,self.maxX,self.maxY)
            self.grasses.append(grass)

    def add_obstacles(self, positionsObstacle) :
        for position in positionsObstacle :
            self.add_obstacle(position, True)

    def add_obstacle(self, positionObstacle, with_image) :
        x, y = positionObstacle
        width, height = self.get_shape(with_image)
        self.obstacles.append(Obstacle(x,y, width,height, with_image))

    def get_shape(self, with_image) :
        if with_image :
            return 40, 40
        else : 
            return 20, 20

    def init_antHills(self, antQueens) :
        for queen in antQueens : 
            self.antHills.append(AntHill(queen.coordinate[0], queen.coordinate[1], queen.colonieId, queen.color))

    def regrowEatenGrasses(self):
        for grass in self.grasses:
            if grass.isEaten:
                grass.isEaten = False
                if self.shouldGrowCoordinate != []:
                    selectedZone = random.choice(self.shouldGrowCoordinate)
                    grass.coordinate[0] = random.randint(selectedZone[0]-self.grassZoneEditRadius,selectedZone[0]+self.grassZoneEditRadius)
                    grass.coordinate[1] = random.randint(selectedZone[1] - self.grassZoneEditRadius,selectedZone[1] + self.grassZoneEditRadius)
                else:

                    r = random.random()
                    if r > 0.5:
                        r = random.random()
                        grass.coordinate[0] = random.randint(0, self.maxX)
                        if r > 0.5:
                            grass.coordinate[1] = random.randint(0, 100)
                        else:
                            grass.coordinate[1] = random.randint(self.maxY - 100, self.maxY)
                    else:
                        r = random.random()
                        grass.coordinate[1] = random.randint(0, self.maxY)
                        if r > 0.5:
                            grass.coordinate[0] = random.randint(0, 100)
                        else:
                            grass.coordinate[0] = random.randint(self.maxX - 100, self.maxX)

    def isGoingThroughWall(self,cells):
        for cell in cells:
            if cell.coordinate[0]<0:
                cell.coordinate[0] = 0
            if cell.coordinate[0]>self.maxX:
                cell.coordinate[0] = self.maxX
            if cell.coordinate[1]<0:
                cell.coordinate[1]=0
            if cell.coordinate[1]>self.maxY:
                cell.coordinate[1]=self.maxY

    def isGoingThroughObstacles(self,cell):
        for obstacle in self.obstacles :
            isCollide = obstacle.shape.collidepoint(cell.coordinate[0], cell.coordinate[1])
            if isCollide : return True
        return False
