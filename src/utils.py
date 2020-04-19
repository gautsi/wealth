"""
Utility functions
"""
import pandas as pd


def fix_to_range(num, minimum, maximum):
    '''fix num to be between minimum and maximum'''
    return minimum if num < minimum else maximum if num > maximum else num

def list_to_json(l):
    '''convert a list of wealths into a json dictionary of wealth info'''
    return [{"person": i, "wealths": [{"time_step": 0, "wealth": j}]} for i, j in enumerate(l)]

def get_wealth(person, time_stamp):
    return {"person": person["person"], "wealth": [i["wealth"] for i in person["wealths"] if i["time_step"] == time_stamp][0]}

def get_wealths(w, time_step):
    return [get_wealth(p, time_step) for p in w.w]


def get_latest_wealth(person):
    latest_wealth = None
    for ts_wealth in person["wealths"]:
        if latest_wealth is None or ts_wealth["time_step"] > latest_wealth["time_step"]:
            latest_wealth = ts_wealth
    return latest_wealth

def group(pcnt_rank):
    if pcnt_rank < 0.5:
        return "lower"
    if pcnt_rank > 0.9:
        return "higher"
    else:
        return "middle"


def add_group(w, time_step):
    ws = get_wealths(w, time_step)
    num_p = len(ws)
    ws_sorted = sorted(ws, key=lambda x: x["wealth"])
    for i, j in enumerate(ws_sorted):
        person = [p for p in w.w if p["person"] == j["person"]][0]
        ts = [t for t in person["wealths"] if t["time_step"] == time_step][0]
        ts["pcnt_rank"] = 1.0 * i / num_p
        ts["group"] = group(ts["pcnt_rank"])
        
    
def group_stats(wealths):
    add_group(wealths)
    groups = wealths.groupby(["time_step", "group"], as_index = False).wealth.sum()
    groups["ttl_wealth"] = groups[["time_step"]].merge(
        right = groups.groupby(["time_step"], as_index = False).wealth.sum(),
        on = ["time_step"],
        how="left")["wealth"]
    groups["group_pct"] = groups.wealth / groups.ttl_wealth
    return groups