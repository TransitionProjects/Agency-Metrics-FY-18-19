"""
Takes dataframes from various ART reports and identifies the fiscal year and
quarter of each row of data, returning the results as a new dataframe object
"""

from datetime import datetime

import pandas as pd
import numpy as np

class QuarterAndFiscalYear:
    def __init__(
        self,
        dataframe,
        exit_date_fill_type=False,
        exit_date_fill=datetime(year=2018, month=7, day=1),
        fill_na=True
    ):
        """
        :dataframe: a pandas dataframe object created from an HMIS ART excel file
        :exit_date_fill_type: a string either "today" or "specify"; default is False
        :exit_date_fill: a datetime.datetime object; default value of
        July 1st, 2018
        :fill_na: a boolean; default is True
        """
        self.dataframe = dataframe
        self.exit_date_fill_type = exit_date_fill_type
        self.exit_fill = exit_date_fill
        self.fill_na = fill_na

        # a dictionary specifying months, years, and their associated ficsal
        # year based upon the federal HUD FY
        self.fiscal_years = fiscal_years = {
            1: {
                2000: "FY 99-00",
                2001: "FY 00-01",
                2002: "FY 01-02",
                2003: "FY 02-03",
                2004: "FY 03-04",
                2005: "FY 04-05",
                2006: "FY 05-06",
                2007: "FY 06-07",
                2008: "FY 07-08",
                2009: "FY 08-09",
                2010: "FY 09-10",
                2011: "FY 10-11",
                2012: "FY 11-12",
                2013: "FY 12-13",
                2014: "FY 13-14",
                2015: "FY 14-15",
                2016: "FY 15-16",
                2017: "FY 16-17",
                2018: "FY 17-18",
                2019: "FY 18-19",
                2020: "FY 19-20",
                2021: "FY 20-21",
                2022: "FY 21-22",
                2023: "FY 22-23",
                2024: "FY 23-24",
                2025: "FY 24-25",
                2026: "FY 25-26",
                2027: "FY 26-27",
                2028: "FY 27-28",
                2029: "FY 28-29",
                2030: "FY 29-30"
            },
            2: {
                2000: "FY 99-00",
                2001: "FY 00-01",
                2002: "FY 01-02",
                2003: "FY 02-03",
                2004: "FY 03-04",
                2005: "FY 04-05",
                2006: "FY 05-06",
                2007: "FY 06-07",
                2008: "FY 07-08",
                2009: "FY 08-09",
                2010: "FY 09-10",
                2011: "FY 10-11",
                2012: "FY 11-12",
                2013: "FY 12-13",
                2014: "FY 13-14",
                2015: "FY 14-15",
                2016: "FY 15-16",
                2017: "FY 16-17",
                2018: "FY 17-18",
                2019: "FY 18-19",
                2020: "FY 19-20",
                2021: "FY 20-21",
                2022: "FY 21-22",
                2023: "FY 22-23",
                2024: "FY 23-24",
                2025: "FY 24-25",
                2026: "FY 25-26",
                2027: "FY 26-27",
                2028: "FY 27-28",
                2029: "FY 28-29",
                2030: "FY 29-30"
            },
            3: {
                2000: "FY 99-00",
                2001: "FY 00-01",
                2002: "FY 01-02",
                2003: "FY 02-03",
                2004: "FY 03-04",
                2005: "FY 04-05",
                2006: "FY 05-06",
                2007: "FY 06-07",
                2008: "FY 07-08",
                2009: "FY 08-09",
                2010: "FY 09-10",
                2011: "FY 10-11",
                2012: "FY 11-12",
                2013: "FY 12-13",
                2014: "FY 13-14",
                2015: "FY 14-15",
                2016: "FY 15-16",
                2017: "FY 16-17",
                2018: "FY 17-18",
                2019: "FY 18-19",
                2020: "FY 19-20",
                2021: "FY 20-21",
                2022: "FY 21-22",
                2023: "FY 22-23",
                2024: "FY 23-24",
                2025: "FY 24-25",
                2026: "FY 25-26",
                2027: "FY 26-27",
                2028: "FY 27-28",
                2029: "FY 28-29",
                2030: "FY 29-30"
            },
            4: {
                2000: "FY 99-00",
                2001: "FY 00-01",
                2002: "FY 01-02",
                2003: "FY 02-03",
                2004: "FY 03-04",
                2005: "FY 04-05",
                2006: "FY 05-06",
                2007: "FY 06-07",
                2008: "FY 07-08",
                2009: "FY 08-09",
                2010: "FY 09-10",
                2011: "FY 10-11",
                2012: "FY 11-12",
                2013: "FY 12-13",
                2014: "FY 13-14",
                2015: "FY 14-15",
                2016: "FY 15-16",
                2017: "FY 16-17",
                2018: "FY 17-18",
                2019: "FY 18-19",
                2020: "FY 19-20",
                2021: "FY 20-21",
                2022: "FY 21-22",
                2023: "FY 22-23",
                2024: "FY 23-24",
                2025: "FY 24-25",
                2026: "FY 25-26",
                2027: "FY 26-27",
                2028: "FY 27-28",
                2029: "FY 28-29",
                2030: "FY 29-30"
            },
            5: {
                2000: "FY 99-00",
                2001: "FY 00-01",
                2002: "FY 01-02",
                2003: "FY 02-03",
                2004: "FY 03-04",
                2005: "FY 04-05",
                2006: "FY 05-06",
                2007: "FY 06-07",
                2008: "FY 07-08",
                2009: "FY 08-09",
                2010: "FY 09-10",
                2011: "FY 10-11",
                2012: "FY 11-12",
                2013: "FY 12-13",
                2014: "FY 13-14",
                2015: "FY 14-15",
                2016: "FY 15-16",
                2017: "FY 16-17",
                2018: "FY 17-18",
                2019: "FY 18-19",
                2020: "FY 19-20",
                2021: "FY 20-21",
                2022: "FY 21-22",
                2023: "FY 22-23",
                2024: "FY 23-24",
                2025: "FY 24-25",
                2026: "FY 25-26",
                2027: "FY 26-27",
                2028: "FY 27-28",
                2029: "FY 28-29",
                2030: "FY 29-30"
            },
            6: {
                2000: "FY 99-00",
                2001: "FY 00-01",
                2002: "FY 01-02",
                2003: "FY 02-03",
                2004: "FY 03-04",
                2005: "FY 04-05",
                2006: "FY 05-06",
                2007: "FY 06-07",
                2008: "FY 07-08",
                2009: "FY 08-09",
                2010: "FY 09-10",
                2011: "FY 10-11",
                2012: "FY 11-12",
                2013: "FY 12-13",
                2014: "FY 13-14",
                2015: "FY 14-15",
                2016: "FY 15-16",
                2017: "FY 16-17",
                2018: "FY 17-18",
                2019: "FY 18-19",
                2020: "FY 19-20",
                2021: "FY 20-21",
                2022: "FY 21-22",
                2023: "FY 22-23",
                2024: "FY 23-24",
                2025: "FY 24-25",
                2026: "FY 25-26",
                2027: "FY 26-27",
                2028: "FY 27-28",
                2029: "FY 28-29",
                2030: "FY 29-30"
            },
            7: {
                2000: "FY 00-01",
                2001: "FY 01-02",
                2002: "FY 02-03",
                2003: "FY 03-04",
                2004: "FY 04-05",
                2005: "FY 05-06",
                2006: "FY 06-07",
                2007: "FY 07-08",
                2008: "FY 08-09",
                2009: "FY 09-10",
                2010: "FY 10-11",
                2011: "FY 11-12",
                2012: "FY 12-13",
                2013: "FY 13-14",
                2014: "FY 14-15",
                2015: "FY 15-16",
                2016: "FY 16-17",
                2017: "FY 17-18",
                2018: "FY 18-19",
                2019: "FY 19-20",
                2020: "FY 20-21",
                2021: "FY 21-22",
                2022: "FY 22-23",
                2023: "FY 23-24",
                2024: "FY 24-25",
                2025: "FY 25-26",
                2026: "FY 26-27",
                2027: "FY 27-28",
                2028: "FY 28-29",
                2029: "FY 29-30",
                2030: "FY 30-31"
            },
            8: {
                2000: "FY 00-01",
                2001: "FY 01-02",
                2002: "FY 02-03",
                2003: "FY 03-04",
                2004: "FY 04-05",
                2005: "FY 05-06",
                2006: "FY 06-07",
                2007: "FY 07-08",
                2008: "FY 08-09",
                2009: "FY 09-10",
                2010: "FY 10-11",
                2011: "FY 11-12",
                2012: "FY 12-13",
                2013: "FY 13-14",
                2014: "FY 14-15",
                2015: "FY 15-16",
                2016: "FY 16-17",
                2017: "FY 17-18",
                2018: "FY 18-19",
                2019: "FY 19-20",
                2020: "FY 20-21",
                2021: "FY 21-22",
                2022: "FY 22-23",
                2023: "FY 23-24",
                2024: "FY 24-25",
                2025: "FY 25-26",
                2026: "FY 26-27",
                2027: "FY 27-28",
                2028: "FY 28-29",
                2029: "FY 29-30",
                2030: "FY 30-31"
            },
            9: {
                2000: "FY 00-01",
                2001: "FY 01-02",
                2002: "FY 02-03",
                2003: "FY 03-04",
                2004: "FY 04-05",
                2005: "FY 05-06",
                2006: "FY 06-07",
                2007: "FY 07-08",
                2008: "FY 08-09",
                2009: "FY 09-10",
                2010: "FY 10-11",
                2011: "FY 11-12",
                2012: "FY 12-13",
                2013: "FY 13-14",
                2014: "FY 14-15",
                2015: "FY 15-16",
                2016: "FY 16-17",
                2017: "FY 17-18",
                2018: "FY 18-19",
                2019: "FY 19-20",
                2020: "FY 20-21",
                2021: "FY 21-22",
                2022: "FY 22-23",
                2023: "FY 23-24",
                2024: "FY 24-25",
                2025: "FY 25-26",
                2026: "FY 26-27",
                2027: "FY 27-28",
                2028: "FY 28-29",
                2029: "FY 29-30",
                2030: "FY 30-31"
            },
            10: {
                2000: "FY 00-01",
                2001: "FY 01-02",
                2002: "FY 02-03",
                2003: "FY 03-04",
                2004: "FY 04-05",
                2005: "FY 05-06",
                2006: "FY 06-07",
                2007: "FY 07-08",
                2008: "FY 08-09",
                2009: "FY 09-10",
                2010: "FY 10-11",
                2011: "FY 11-12",
                2012: "FY 12-13",
                2013: "FY 13-14",
                2014: "FY 14-15",
                2015: "FY 15-16",
                2016: "FY 16-17",
                2017: "FY 17-18",
                2018: "FY 18-19",
                2019: "FY 19-20",
                2020: "FY 20-21",
                2021: "FY 21-22",
                2022: "FY 22-23",
                2023: "FY 23-24",
                2024: "FY 24-25",
                2025: "FY 25-26",
                2026: "FY 26-27",
                2027: "FY 27-28",
                2028: "FY 28-29",
                2029: "FY 29-30",
                2030: "FY 30-31"
            },
            11: {
                2000: "FY 00-01",
                2001: "FY 01-02",
                2002: "FY 02-03",
                2003: "FY 03-04",
                2004: "FY 04-05",
                2005: "FY 05-06",
                2006: "FY 06-07",
                2007: "FY 07-08",
                2008: "FY 08-09",
                2009: "FY 09-10",
                2010: "FY 10-11",
                2011: "FY 11-12",
                2012: "FY 12-13",
                2013: "FY 13-14",
                2014: "FY 14-15",
                2015: "FY 15-16",
                2016: "FY 16-17",
                2017: "FY 17-18",
                2018: "FY 18-19",
                2019: "FY 19-20",
                2020: "FY 20-21",
                2021: "FY 21-22",
                2022: "FY 22-23",
                2023: "FY 23-24",
                2024: "FY 24-25",
                2025: "FY 25-26",
                2026: "FY 26-27",
                2027: "FY 27-28",
                2028: "FY 28-29",
                2029: "FY 29-30",
                2030: "FY 30-31"
            },
            12: {
                2000: "FY 00-01",
                2001: "FY 01-02",
                2002: "FY 02-03",
                2003: "FY 03-04",
                2004: "FY 04-05",
                2005: "FY 05-06",
                2006: "FY 06-07",
                2007: "FY 07-08",
                2008: "FY 08-09",
                2009: "FY 09-10",
                2010: "FY 10-11",
                2011: "FY 11-12",
                2012: "FY 12-13",
                2013: "FY 13-14",
                2014: "FY 14-15",
                2015: "FY 15-16",
                2016: "FY 16-17",
                2017: "FY 17-18",
                2018: "FY 18-19",
                2019: "FY 19-20",
                2020: "FY 20-21",
                2021: "FY 21-22",
                2022: "FY 22-23",
                2023: "FY 23-24",
                2024: "FY 24-25",
                2025: "FY 25-26",
                2026: "FY 26-27",
                2027: "FY 27-28",
                2028: "FY 28-29",
                2029: "FY 29-30",
                2030: "FY 30-31"
            }
        }

        # a dictionary specifying months and their associated ficsal
        # year based upon the federal HUD FY
        self.quarters = {
            1: "Q3",
            2: "Q3",
            3: "Q3",
            4: "Q4",
            5: "Q4",
            6: "Q4",
            7: "Q1",
            8: "Q1",
            9: "Q1",
            10: "Q2",
            11: "Q2",
            12: "Q2"
        }

    def get_datetime_column_names(self):
        """
        :return: A list of names of columns that contain the datetime64[ns] dtypes
        """
        return self.dataframe.select_dtypes(
            include=["datetime64[ns]"]
        ).columns.get_values().tolist()

    def follow_fill_command(self):
        """
        Fill the nan values in columns with dtypes of datetime64[ns]
        :return: a pandas dataframe
        """
        # make a local copy of the self.dataframe object
        data = self.dataframe

        # check the class parameters and fill the nan values in the datetime64[ns]
        # columns appropriatly
        if self.fill_na and (self.exit_date_fill_type == "today"):
            for column in self.get_datetime_column_names():
                data[column].fillna(datetime.today(), inplace=True)
        elif self.fill_na and (self.exit_date_fill_type == "specify"):
            for column in self.get_datetime_column_names():
                data[column].fillna(self.exit_fill, inplace=True)
        else:
            pass

        return data

    def create_fy_q_columns(self):
        """
        Create fiscal year and quarter columns for each of the datetime64[ns]
        columns, then fill those columns with the appropriate quarter or fiscal
        year.
        :return: a pandas dataframe
        """
        # make a local copy of the self.dataframe object
        data = self.follow_fill_command()

        # loop through the columns that have a dtype of datetime64[ns]
        for name in self.get_datetime_column_names():

            # create fiscal year and quarter columns for each relevant column
            y_value = name + " Fiscal Year"
            q_value = name + " Quarter"

            # fill the fiscal year values
            data[y_value] = [
                self.fiscal_years[month][year] for (month, year) in list(
                    zip(
                        data[name].dt.month,
                        data[name].dt.year
                    )
                )
            ]

            # fill the quarter values
            data[q_value] = [
                self.quarters[month] for month in data[name].dt.month
            ]

        return data
