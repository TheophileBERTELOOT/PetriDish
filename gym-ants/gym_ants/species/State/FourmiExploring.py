from .FourmiState import FourmiState, FourmiStateName

class FourmiExploring(FourmiState):
    
    def __init__(self, fourmi):
        
        FourmiState.__init__(self, FourmiStateName.EXPLORING)
        self.fourmi = fourmi
        
    def check_conditions(self, grasses):        
        if (self.fourmi.isSmellingGrasses(grasses)) :
            return FourmiStateName.FINDING
        return None

    def get_reward(self):
        return -1
        