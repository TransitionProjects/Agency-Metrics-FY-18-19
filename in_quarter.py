"""

"""

import pandas as pd
import numpy as np
from datetime import datetime

def return_quarters(entry_df):
    # set up a dict of quarter date ranges
    # this will need to be updated annually
    quarters = {
        "Q1": [datetime(year=2018, month=6, day=30), datetime(year=2018, month=10, day=1)],
        "Q2": [datetime(year=2018, month=9, day=30), datetime(year=2019, month=1, day=1)],
        "Q3": [datetime(year=2018, month=12, day=31), datetime(year=2019, month=4, day=1)],
        "Q4": [datetime(year=2019, month=3, day=31), datetime(year=2019, month=7, day=1)]
    }

    # create a local copy of the entries_df
    df = entry_df

    # create quarter start and end columns for comparison
    df["Q1 Start"] = quarters["Q1"][0]
    df["Q1 End"] = quarters["Q1"][1]
    df["Q2 Start"] = quarters["Q2"][0]
    df["Q2 End"] = quarters["Q2"][1]
    df["Q3 Start"] = quarters["Q3"][0]
    df["Q3 End"] = quarters["Q3"][1]
    df["Q4 Start"] = quarters["Q4"][0]
    df["Q4 End"] = quarters["Q4"][1]

    # use numpy.select method for adding Q1-Q4 columns with binary values
    q1_conditions = [
        (
            (df["Entry Exit Entry Date"] > df["Q1 Start"]) &
            (df["Entry Exit Exit Date"] < df["Q1 End"])
        ),
        (
            (df["Entry Exit Entry Date"] < df["Q1 Start"]) &
            (df["Entry Exit Exit Date"] > df["Q1 Start"]) &
            (df["Entry Exit Exit Date"] < df["Q1 End"])
        ),
        (
            (df["Entry Exit Entry Date"] < df["Q1 Start"]) &
            (df["Entry Exit Exit Date"] > df["Q1 End"])
        ),
        (
            (df["Entry Exit Entry Date"] > df["Q1 Start"]) &
            (df["Entry Exit Entry Date"] < df["Q1 End"]) &
            (df["Entry Exit Exit Date"] > df["Q1 End"])
        ),
        (
            df["Entry Exit Exit Date"] < df["Q1 Start"]
        ),
        (
            df["Entry Exit Entry Date"] > df["Q1 End"]
        ),
        (df["Entry Exit Entry Date"] == df["Q1 Start"]),
        (df["Entry Exit Exit Date"] == df["Q1 End"])
    ]
    q2_conditions = [
        (
            (df["Entry Exit Entry Date"] > df["Q2 Start"]) &
            (df["Entry Exit Exit Date"] < df["Q2 End"])
        ),
        (
            (df["Entry Exit Entry Date"] < df["Q2 Start"]) &
            (df["Entry Exit Exit Date"] > df["Q2 Start"]) &
            (df["Entry Exit Exit Date"] < df["Q2 End"])
        ),
        (
            (df["Entry Exit Entry Date"] < df["Q2 Start"]) &
            (df["Entry Exit Exit Date"] > df["Q2 End"])
        ),
        (
            (df["Entry Exit Entry Date"] > df["Q2 Start"]) &
            (df["Entry Exit Entry Date"] < df["Q2 End"]) &
            (df["Entry Exit Exit Date"] > df["Q2 End"])
        ),
        (
            df["Entry Exit Exit Date"] < df["Q2 Start"]
        ),
        (
            df["Entry Exit Entry Date"] > df["Q2 End"]
        ),
        (df["Entry Exit Entry Date"] == df["Q2 Start"]),
        (df["Entry Exit Exit Date"] == df["Q2 End"])
    ]
    q3_conditions = [
        (
            (df["Entry Exit Entry Date"] > df["Q3 Start"]) &
            (df["Entry Exit Exit Date"] < df["Q3 End"])
        ),
        (
            (df["Entry Exit Entry Date"] < df["Q3 Start"]) &
            (df["Entry Exit Exit Date"] > df["Q3 Start"]) &
            (df["Entry Exit Exit Date"] < df["Q3 End"])
        ),
        (
            (df["Entry Exit Entry Date"] < df["Q3 Start"]) &
            (df["Entry Exit Exit Date"] > df["Q3 End"])
        ),
        (
            (df["Entry Exit Entry Date"] > df["Q3 Start"]) &
            (df["Entry Exit Entry Date"] < df["Q3 End"]) &
            (df["Entry Exit Exit Date"] > df["Q3 End"])
        ),
        (
            df["Entry Exit Exit Date"] < df["Q3 Start"]
        ),
        (
            df["Entry Exit Entry Date"] > df["Q3 End"]
        ),
        (df["Entry Exit Entry Date"] == df["Q3 Start"]),
        (df["Entry Exit Exit Date"] == df["Q3 End"])
    ]
    q4_conditions = [
        (
            (df["Entry Exit Entry Date"] > df["Q4 Start"]) &
            (df["Entry Exit Exit Date"] < df["Q4 End"])
        ),
        (
            (df["Entry Exit Entry Date"] < df["Q4 Start"]) &
            (df["Entry Exit Exit Date"] > df["Q4 Start"]) &
            (df["Entry Exit Exit Date"] < df["Q4 End"])
        ),
        (
            (df["Entry Exit Entry Date"] < df["Q4 Start"]) &
            (df["Entry Exit Exit Date"] > df["Q4 End"])
        ),
        (
            (df["Entry Exit Entry Date"] > df["Q4 Start"]) &
            (df["Entry Exit Entry Date"] < df["Q4 End"]) &
            (df["Entry Exit Exit Date"] > df["Q4 End"])
        ),
        (
            df["Entry Exit Exit Date"] < df["Q4 Start"]
        ),
        (
            df["Entry Exit Entry Date"] > df["Q1 End"]
        ),
        (df["Entry Exit Entry Date"] == df["Q4 Start"]),
        (df["Entry Exit Exit Date"] == df["Q4 End"])
    ]

    choices = [1, 1, 1, 1, 0, 0, 1, 1]
    df["Q1"] = np.select(q1_conditions, choices)
    df["Q2"] = np.select(q2_conditions, choices)
    df["Q3"] = np.select(q3_conditions, choices)
    df["Q4"] = np.select(q4_conditions, choices)

    return df
