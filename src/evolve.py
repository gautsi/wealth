"""
Wealth evolution functions
"""
import numpy as np
from src import utils

@utils.evolve_one_to_all
def uniform_value(wealth, min_value=0, max_value=1):
    '''assume wealth at each time step is uniformly distributed from min_value to max_value'''
    return np.random.uniform(low=min_value, high=max_value)

@utils.evolve_one_to_all
def uniform_change(wealth, min_change=-1, max_change=1):
    '''assume absolute wealth change is uniformly distributed from min_change to max_change'''
    change = np.random.uniform(low=min_change, high=max_change)
    return wealth + change


@utils.evolve_one_to_all
def normal_change(wealth, loc=0, scale=0.1):
    '''assume percent wealth change is normally distributed around loc with standard deviation scale'''
    pcnt_change = np.random.normal(loc=loc, scale=scale)
    # assume maximum percent increase is 100% (double the wealth), min is -100% (lose all wealth)
    return wealth + utils.fix_to_range(pcnt_change, -1, 1) * wealth


