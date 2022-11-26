from .FourmiState import FourmiState, FourmiStateName

class FourmiFeeding(FourmiState):
    
    def __init__(self, fourmi):
        
        FourmiState.__init__(self, FourmiStateName.FEEDING)
        self.fourmi = fourmi

        
    def check_conditions(self, grasses):
        if(not self.fourmi.foodCarried):
            return FourmiStateName.EXPLORING       

        return None

    def get_reward(self):
        return 0