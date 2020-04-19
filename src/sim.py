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
    def __init__(self, w, ev):
        """
        Parameters
        ----------
        - w (wealths.Wealths): wealth info
        - ev (evolve.Evolve): specify how to evolve wealth
        """
        self.w = w
        self.ev = ev
        self.time_step = 0
        utils.add_group(self.w, self.time_step)
    
    def step(self, n=1):
        '''evolve all wealth values by n time steps'''
        for i in tqdm(range(n)):
            self.ev.apply(self.w)
            self.time_step += 1
            utils.add_group(self.w, self.time_step)
    
    def hist(self, time_step=0):
        fig, ax = plt.subplots(figsize=(10,5))
        ax.hist(self.wealths[self.wealths.time_step == time_step].wealth, color="steelblue", bins = 20)
        return fig, ax