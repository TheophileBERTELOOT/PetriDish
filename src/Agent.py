import random
import numpy as np
class EGreedy:
    def __init__(self,nbAction,T):
        self.nbAction = nbAction
        self.epsilon=random.random()
        self.T=T
        self.muChapeau = [0 for _ in range(nbAction)]
        self.nbTimePlayed = [0 for _ in range(nbAction)]
        self.lastPlayedAction=0

    def play(self,cell,food):
        selectedAction=-1

        for actionIndex in range(self.nbAction):
            if self.nbTimePlayed[actionIndex]==0:
                selectedAction = actionIndex
        if selectedAction == -1:
            r = random.random()
            if r <= self.epsilon:
                selectedAction = random.randint(0, self.nbAction-1)
            else:
                tempMuChapeau = [self.muChapeau[i] / self.nbTimePlayed[i] for i in range(self.nbAction)]
                selectedAction = np.argmax(tempMuChapeau)
        self.applyAction(cell,selectedAction)
        cell.eat(food)
        self.muChapeau[selectedAction] += cell.hasEaten
        if sum(self.nbTimePlayed)<self.T:
            self.nbTimePlayed[selectedAction] += 1


    def applyAction(self,cell,selectedAction):
        if cell.dx>=0 and cell.dy>=0:
            angle = np.arccos(cell.dx)
        if cell.dx<=0 and cell.dy>=0:
            angle = np.arccos(cell.dx)
        if cell.dx>=0 and cell.dy<=0:
            angle = -np.arcsin(cell.dx)
        if cell.dx<=0 and cell.dy<=0:
            angle = -np.arccos(cell.dx)


        if selectedAction == 0:
            angle+=np.pi/12
        else:
            angle-=np.pi/12
        cell.dx=np.cos(angle)
        cell.dy=np.sin(angle)
        cell.normalize()

