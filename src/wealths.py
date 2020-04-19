"""
Organizing wealths
"""

import numpy as np
import pandas as pd
from src import utils
from tqdm import tqdm
from matplotlib import pyplot as plt
plt.style.use("seaborn")

class Wealths(object):
    def __init__(self, initial_wealth):
        """
        Parameters
        ----------
        - initial_wealth (list[float]): inital wealth values
        """
        self.initial_wealth = initial_wealth
        self.w = utils.list_to_json(initial_wealth)

    def group_stats(self):
        ts_stats = []
        for p in self.w:
            for ts in p["wealths"]:
                find_ts = [t for t in ts_stats if t["time_step"] == ts["time_step"]]
                if len(find_ts) == 0:
                    ts_stats.append({"time_step": ts["time_step"], "wealths": {"total": ts["wealth"], ts["group"]: ts["wealth"]}})
                else:
                    find_ts[0]["wealths"]["total"] += ts["wealth"]
                    if ts["group"] in find_ts[0]["wealths"].keys():
                        find_ts[0]["wealths"][ts["group"]] += ts["wealth"]
                    else:
                        find_ts[0]["wealths"][ts["group"]] = ts["wealth"]
        for ts in ts_stats:
            for g in ["lower", "middle", "higher"]:
                ts["wealths"]["{}_pcnt".format(g)] = ts["wealths"][g] / ts["wealths"]["total"]
        return ts_stats
    
    def wealths_over_time(self):
        fig, ax = plt.subplots(figsize=(10,5))
        for person in self.w:
            ws = [i["wealth"] for i in person["wealths"]]
            ts = [i["time_step"] for i in person["wealths"]]
            ax.plot(ts, ws, color="steelblue", alpha=0.2)
        return fig, ax
            
    def hist(self, time_step=0):
        fig, ax = plt.subplots(figsize=(10,5))
        ax.hist([i["wealth"] for i in utils.get_wealths(self, time_step)], color="steelblue", bins = 20)
        return fig, ax
    
    def groups_over_time(self):
        gs = self.group_stats()
        fig, ax = plt.subplots(figsize=(10, 5))
        for c in ["lower", "middle", "higher"]:
            group_data = groups[(groups["group"] == c) & (groups.time_step > 0)].sort_values("time_step")
            ax.plot(group_data.time_step, group_data.group_pct, linewidth = 2, label = c)
        ax.legend()
        return fig, ax

    def __repr__(self):
        return self.w[:10].__repr__() + ("..." if len(self.w) > 10 else "")