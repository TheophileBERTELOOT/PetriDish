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

    def play(self,cell,grasses):
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
        cell.eat(grasses)
        self.muChapeau[selectedAction] += cell.hasEaten
        if sum(self.nbTimePlayed)<self.T:
            self.nbTimePlayed[selectedAction] += 1


    def applyAction(self,cell,selectedAction):
        if selectedAction == 0:
            cell.dx+=0.01
            cell.dy+=0.01
        else:
            cell.dx-=0.01
            cell.dy-=0.01

