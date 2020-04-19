"""
Organize wealth evolution
"""
import numpy as np
from src import utils

class Evolve(object):
    def __init__(self, evolve_functions):
        '''
        Parameters
        ----------
        - evolve_fumctions ([list[callable[Wealths]]]): functions to apply to wealth info to evolve wealths, applied in order (first function applied first, second applied second, ...)
        '''
        self.evolve_functions = evolve_functions
    
    def apply(self, w):
        '''
        evolve a Wealth object by applying evolve functions in order
        '''
        for f in self.evolve_functions:
            f(w.w)
            

def evolve_one_to_all(f):
    '''decorator: apply wealth evolution function f that evolves a singe wealth to all wealths in a Wealth object'''
    def wrapper(w, *args, **kwargs):
        # get latest wealth
        for person in w:
            latest_wealth = utils.get_latest_wealth(person)
            person["wealths"].append({"time_step": latest_wealth["time_step"] + 1, "wealth": f(latest_wealth["wealth"], *args, **kwargs)})
    return wrapper


@evolve_one_to_all
def uniform_value(wealth, min_value=0, max_value=1):
    '''assume wealth at each time step is uniformly distributed from min_value to max_value'''
    return np.random.uniform(low=min_value, high=max_value)

@evolve_one_to_all
def uniform_change(wealth, min_change=-1, max_change=1):
    '''assume absolute wealth change is uniformly distributed from min_change to max_change'''
    change = np.random.uniform(low=min_change, high=max_change)
    return wealth + change


@evolve_one_to_all
def normal_change(wealth, loc=0, scale=0.1):
    '''assume percent wealth change is normally distributed around loc with standard deviation scale'''
    pcnt_change = np.random.normal(loc=loc, scale=scale)
    # assume maximum percent increase is 100% (double the wealth), min is -100% (lose all wealth)
    return wealth + utils.fix_to_range(pcnt_change, -1, 1) * wealth
