"""
Utility functions
"""
import pandas as pd


wealth_fields_order = ["person", "time_step", "wealth"] # field order for wealth DataFrames

def fix_to_range(num, minimum, maximum):
    '''fix num to be between minimum and maximum'''
    return minimum if num < minimum else maximum if num > maximum else num

def list_to_dataframe(f):
    '''decorator: convert a list of wealths into a dataframe, f is a function that returns a list of wealths'''
    def wrapper(*args, **kwargs):
        l = f(*args, **kwargs)
        return pd.DataFrame({"person": range(len(l)), "wealth": l})
    return wrapper

def evolve_one_to_all(f):
    '''decorator: apply wealth evolution function f that evolves a singe wealth to a wealth DataFrame'''
    def wrapper(df, *args, **kwargs):
        # get current wealth values
        curr_wealths = df[df.time_step == df.time_step.max()]
        # evolve all current wealth values
        curr_wealths["wealth"] = curr_wealths.wealth.map(lambda x: f(x, *args, **kwargs))
        # add new values to the dataframe
        return pd.concat([df, curr_wealths.assign(time_step = df.time_step.max() + 1)[wealth_fields_order]])
    return wrapper

def add_pcnt_rank(wealths):
    wealths["pct_rank"] = wealths.groupby(["time_step"]).wealth.rank(pct=True)
    
def group(pct_rank):
    if pct_rank < 0.5:
        return "lower"
    if pct_rank > 0.9:
        return "higher"
    else:
        return "middle"
    
def add_group(wealths):
    add_pcnt_rank(wealths)
    wealths["group"] = wealths.pct_rank.map(group)
    
def group_stats(wealths):
    add_group(wealths)
    groups = wealths.groupby(["time_step", "group"], as_index = False).wealth.sum()
    groups["ttl_wealth"] = groups[["time_step"]].merge(
        right = groups.groupby(["time_step"], as_index = False).wealth.sum(),
        on = ["time_step"],
        how="left")["wealth"]
    groups["group_pct"] = groups.wealth / groups.ttl_wealth
    return groups