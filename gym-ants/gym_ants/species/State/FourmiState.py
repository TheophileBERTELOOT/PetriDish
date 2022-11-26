from enum import Enum

class FourmiStateName(Enum) :
    EXPLORING = 0
    FINDING = 1
    FEEDING = 2

class FourmiState(object):
    
    def __init__(self, name):        
        self.name = name
        
    def do_actions(self):
        pass
        
    def check_conditions(self, grasses):        
        pass    
    
    def entry_actions(self):        
        pass    
    
    def exit_actions(self):        
        pass
    
    def get_reward(self):
        pass