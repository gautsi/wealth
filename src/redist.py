"""
Redistribution functions
"""

import numpy as np
import pandas as pd
from src import utils

def lottery(df, tax_rate=0.2, reg=10):
    curr_time_step = df.time_step.max()
    if curr_time_step % reg == 0:
        curr_wealths = df[df.time_step == curr_time_step]
        # collect tax
        curr_wealths["tax"] = curr_wealths.wealth * tax_rate
        curr_wealths["post_tax"] = curr_wealths.wealth - curr_wealths.tax
        # distribute
        funds = curr_wealths["tax"].sum()
        curr_wealths["lottery"] = curr_wealths.wealth.map(lambda x: np.random.uniform(low=0, high=1))
        curr_wealths["lottery_pcnt"] = curr_wealths.lottery / curr_wealths.lottery.sum()
        curr_wealths["wealth"] = curr_wealths.post_tax + curr_wealths.lottery_pcnt * funds
        # replace values in the dataframe
        return pd.concat([df[df.time_step != curr_time_step], curr_wealths[utils.wealth_fields_order]])
    else:
        return df