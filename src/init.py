"""
Wealth initializations
"""

from src import utils

def constant(pop=1000, value=10):
    '''constant initial wealth with value value, population pop'''
    return pop*[value]