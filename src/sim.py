"""
Organizing simulations
"""

import numpy as np
import pandas as pd
from src import utils

class Sim(object):
    def __init__(self, init_func, evolve_func, redist_func):
        self.init_func = init_func
        self.evolve_func = evolve_func
        self.redist_func = redist_func
        self.time_step = 0 # tracks iterations
        self.wealth_fields_order = ["person", "time_step", "wealth"] # field order for dataframe
        self.initialize()
    
    def initialize(self):
        self.wealths = self.init_func().assign(time_step = 0)[self.wealth_fields_order]
        
#   def evolve(self, wealth):
#       '''evolve one wealth value by one time step'''
#       
#       # assume percent wealth change is normally distributed around 0 with standard deviation 5%
#       pcnt_change = np.random.normal(loc=0, scale=0.05)
#       # assume maximum percent increase is 100% (double the wealth), min is -100% (lose all wealth)
#       return wealth + utils.fix_to_range(pcnt_change, -1, 1) * wealth
    
    def step(self, n=1):
        '''evolve all wealth values by n time steps'''
        if n == 0:
            return None
#        # get current wealth values
#        curr_wealths = self.wealths[self.wealths.time_step == self.time_step]
#        # evolve all current wealth values
#        curr_wealths["wealth"] = curr_wealths.wealth.map(self.evolve)
#        # add new values to the dataframe
#        self.wealths = pd.concat([self.wealths, curr_wealths.assign(time_step = self.time_step + 1)[self.wealth_fields_order]])
        # update time step
        self.evolve_func()
        self.redist_func()
        self.time_step = self.time_step + 1
        self.step(n-1)