"""
Utility functions
"""

def fix_to_range(num, minimum, maximum):
    '''fix num to be between minimum and maximum'''
    return minimum if num < minimum else maximum if num > maximum else num