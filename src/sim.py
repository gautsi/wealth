"""
Organizing simulations
"""

import numpy as np
import pandas as pd
from src import utils
from tqdm import tqdm
from matplotlib import pyplot as plt
plt.style.use("seaborn")

class Sim(object):
    def __init__(self, initial_wealth, evolve_func, redist_func):
        """
        Parameters
        ----------
        - initial_wealth (pandas.DataFrame): inital wealth values, DataFrame with fields person (person identifier) and wealth (wealth value)
        - evolve_func (function): takes a wealth DataFrame and evolves all wealths by one time step
        - redist_func (function): takes a wealth DataFrame and redistributes all wealths by one time step
        """
        self.initial_wealth = initial_wealth
        self.evolve_func = evolve_func
        self.redist_func = redist_func
        self.time_step = 0 # tracks iterations
        self.wealths = self.initial_wealth.assign(time_step = 0)[utils.wealth_fields_order]
    
        
#   def evolve(self, wealth):
#       '''evolve one wealth value by one time step'''
#       
    
    def step(self, n=1):
        '''evolve all wealth values by n time steps'''
        for i in tqdm(range(n)):
            self.wealths = self.evolve_func(self.wealths)
            self.wealths = self.redist_func(self.wealths)
        # update time step
        self.time_step = self.time_step + n
        
    def wealths_over_time(self):
        fig, ax = plt.subplots(figsize=(10,5))
        for person in self.wealths.person.unique():
            wealths = self.wealths[self.wealths.person == person].sort_values("time_step")
            ax.plot(wealths.time_step, wealths.wealth, color="steelblue", alpha=0.2)
        return fig, ax
    
    def hist(self, time_step=0):
        fig, ax = plt.subplots(figsize=(10,5))
        ax.hist(self.wealths[self.wealths.time_step == time_step].wealth, color="steelblue", bins = 20)
        return fig, ax