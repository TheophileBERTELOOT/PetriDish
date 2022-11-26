

class StateMachine(object):
    
    def __init__(self):
        
        self.states = {}
        self.active_state = None
    
    
    def add_state(self, state):
        
        self.states[state.name] = state
        
        
    def transit(self, grasses):
        
        if self.active_state is None:
            return
        
        new_state_name = self.active_state.check_conditions(grasses)
        if new_state_name is not None:
            self.set_state(new_state_name)
        
    
    def set_state(self, new_state_name):        
          
        self.active_state = self.states[new_state_name]        
        self.active_state.entry_actions()

    def get_reward(self) : 
        self.active_state.get_reward()