from .FourmiState import FourmiState, FourmiStateName

class FourmiFinding(FourmiState):
    
    def __init__(self, fourmi):
        
        FourmiState.__init__(self, FourmiStateName.FINDING)
        self.fourmi = fourmi

        
    def check_conditions(self, grasses):
        if(self.fourmi.foodCarried):
            return FourmiStateName.FEEDING        
        elif ( not self.fourmi.isSmellingGrasses(grasses)) :
            return FourmiStateName.FINDING
        return None

    def get_reward(self):
        return 0