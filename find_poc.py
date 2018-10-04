"""
Identify people of color checking Race, Race-Additional, and Ethnicity columns
then returning a pandas dataframe series object

Any pandas dataframe with the three previously identified columns, as well as
the Client Uid column will work
"""

import pandas as pd
import numpy as np

class CreatePOCList:
    def __init__(self, dataframe):
        """
        dataframe: a pandas dataframe object containing Client Uid, Race,
        Race-Additional, and Ethnicity Hispanic/Latino columns
        """
        self.data = dataframe
        self.poc = [
            "American Indian or Alaska Native (HUD)",
            "Black or African American (HUD)",
            "Native Hawaiian or Other Pacific Islander (HUD)",
            "Other Multi-Racial",
            "Asian (HUD)",
            "Hispanic/Latino (HUD)"
        ]

    def return_poc_list(self):
        """
        Creates a local copy of the self.data dataframe, filters for only
        individuals who identify as a poc in at least one of the non-client uid
        columns, then return a pandas seriese objects of the related client uids

        :return: a pandas series object containing the client uids of
        participants idenifying as poc
        """

        poc = self.data[
            (
                (self.data["Race(895)"].isin(self.poc)) |
                (self.data["Race-Additional(1213)"].isin(self.poc)) |
                (self.data["Ethnicity (Hispanic/Latino)(896)"].isin(self.poc))
            )
        ]
        return poc["Client Uid"].drop_duplicates().tolist()

    def return_poc_pivot(self):
        """
        Create a pivot table showing persons counts of poc by how they idenifying

        :return: a pandas pivot_table object
        """
        pivot1 = pd.pivot_table(
            self.data.drop_duplicates(subset="Client Uid"),
            index=["Race(895)"],
            values="Client Uid",
            aggfunc=[len]
        ).reset_index()
        pivot2 = pd.pivot_table(
            self.data.drop_duplicates(subset="Client Uid"),
            index=["Race-Additional(1213)"],
            values="Client Uid",
            aggfunc=[len]
        ).reset_index()
        pivot3 = pd.pivot_table(
            self.data.drop_duplicates(subset="Client Uid"),
            index=["Ethnicity (Hispanic/Latino)(896)"],
            values="Client Uid",
            aggfunc=[len]
        ).reset_index()

        return pd.merge(
            pd.merge(
                pivot1,
                pivot2,
                how="outer",
                on="Client Uid"
            ),
            pivot3,
            how="outer",
            on="Client Uid"
        )
