"""
Wealth initializations
"""

from src import utils

@utils.list_to_dataframe
def constant(pop=1000, value=10):
    '''constant initial wealth with value value, population pop'''
    return pop*[value]