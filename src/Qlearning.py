import numpy as np
import copy
class Qlearning:
    def __init__(self,nbAction,nbRay,nbType):
        self.nbAction = nbAction
        self.nbRay = nbRay
        self.q_table = np.zeros([1+nbRay,nbAction])
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1
        self.old_value = 0
        self.old_action = 0
        self.oldDistance = []
        self.oldType = []
        self.isFirstTime = True

    def stateFromRayType(self,rayType):
        for rayIndex in range(len(rayType)):
            ray = rayType[rayIndex]
            if ray == 1:
                return rayIndex+1
        return 0

    def calcDistanceReward(self,cell):
        for indexRay in range(len(self.oldDistance)):
            newType = cell.visionRayObject[indexRay]
            oldRayType = self.oldType[indexRay]
            if newType == 1:
                newDistance = cell.visionRayLength[indexRay]
                oldRayDistance = self.oldDistance[indexRay]
                if newDistance<oldRayDistance:
                    return 50
        return -1


    def play(self,cell,food):
        if cell.type != cell.TYPE_OUVRIERE:
            return
        state = self.stateFromRayType(cell.visionRayObject)
        if not self.isFirstTime:
            cell.eat(food)
            if cell.hasEaten:
                reward = 1000
            else:
                reward = self.calcDistanceReward(cell)
            next_max = np.max(self.q_table[state])
            new_value = (1 - self.alpha) * self.old_value + self.alpha * (reward + self.gamma * next_max)
            self.q_table[state, self.action] = new_value
            print(self.q_table)
        self.oldType = copy.deepcopy(cell.visionRayObject)
        self.oldDistance = copy.deepcopy(cell.visionRayLength)
        if np.random.uniform(0,1)<self.epsilon:
            self.action = np.random.randint(0,self.nbAction)
        else:
            self.action = np.argmax(self.q_table[state])
        self.old_value = self.q_table[state, self.action]
        self.applyAction(cell,self.action)
        if self.isFirstTime:
            self.isFirstTime = False

    def applyAction(self, cell, selectedAction):
        angle = cell.angle

        if selectedAction == 0:
            angle+=np.pi/12
            cell.dx = np.cos(angle)
            cell.dy = np.sin(angle)
        elif selectedAction == 1:
            angle-=np.pi/12
            cell.dx = np.cos(angle)
            cell.dy = np.sin(angle)
        else:
            angle = angle
        cell.normalize()