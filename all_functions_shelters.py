"""
A repository of functions that can be used to obtain numbers for the various
agency metrics
"""

import pandas as pd
import numpy as np
from determine_period import QuarterAndFiscalYear
from find_poc import CreatePOCList
from in_quarter import return_quarters
from datetime import datetime
from tkinter.filedialog import askopenfilename, asksaveasfilename

class AllFunctions:
    def __init__(self):
        self.perm_dest = [
            "Owned by client, no ongoing housing subsidy (HUD)",
            "Owned by client, with ongoing housing subsidy (HUD)",
            "Permanent housing for formerly homeless persons (HUD)",
            "Rental by client, no ongoing housing subsidy (HUD)",
            "Rental by client, with other ongoing housing subsidy (HUD)",
            "Rental by client, with VASH subsidy (HUD)",
            "Staying or living with family, permanent tenure (HUD)",
            "Staying or living with friends, permanent tenure (HUD)",
            "Foster care home or foster care group home (HUD)",
            "Rental by client, with GPD TIP subsidy (HUD)",
            "Permanent housing (other than RRH) for formerly homeless persons (HUD)",
            "Moved from one HOPWA funded project to HOPWA PH (HUD)",
            "Long-term care facility or nursing home (HUD)",
            "Residential project or halfway house with no homeless criteria (HUD)"
        ]
        self.temp_dest = [
            "Hospital or other residential non-psychiatric medical facility (HUD)",
            "Hotel or motel paid for without emergency shelter voucher (HUD)",
            "Jail, prison or juvenile detention facility (HUD)",
            "Staying or living with family, temporary tenure (e.g., room, apartment or house)(HUD)",
            "Staying or living with friends, temporary tenure (e.g., room apartment or house)(HUD)",
            "Transitional housing for homeless persons (including homeless youth) (HUD)",
            "Moved from one HOPWA funded project to HOPWA TH (HUD)",
            "Substance abuse treatment facility or detox center (HUD)",
            "Psychiatric hospital or other psychiatric facility (HUD)"
        ]
        self.departments = {
            "rec": [
                "Transition Projects (TPI) - Day Center - SP(26)"
            ],
            "vets": [
                "Transition Projects (TPI) - SSVF_18-OR-399 – Rapid Re-Housing (VA)(6350)",
                "Transition Projects (TPI) Rent - Housing for Veterans (PHB)(5138)",
                "Transition Projects (TPI) - Oregon Vets (OHA) - PSH(5744)",
                "Impact Northwest - SSVF_18-OR-399 – Rapid Re-Housing (VA)(6366)",
                "Transition Projects (TPI) - SSVF_18-OR-399 – Homeless Prevention (VA)(6351)",
                "Transition Projects (TPI) Rent - EHA Vets (STRA) - HP(5794)",
                "Transition Projects (TPI) - SSVF_Renewal 15-ZZ-127 Rapid Re-Housing (VA) - SP(4802)",
                "Impact Northwest - SSVF_Renewal 15-ZZ-127 - Rapid Re-Housing (VA) - SP(4795)",
                "Transition Projects (TPI) - SSVF_Renewal 15-ZZ-127 - Homeless Prevention (VA) - SP(4801)",
                "Transition Projects (TPI) Rent - EHA Vets (STRA) - RRH(4930)",
                "Transition Projects (TPI) - SSVF_C15-OR-501A - Rapid Re-Housing (VA) - SP(4804)",
            ],
            "housing": [
                "Transition Projects (TPI) - ACCESS - CM(5471)",
                "Transition Projects (TPI) - Residential - CM(5473)"
            ],
            "retention": ["Transition Projects (TPI) - Retention - CM(5472)"],
            "agency": [],
            "ca bm": [
                "Transition Projects (TPI) Housing - Clark Annex PSH - SP(2858)",
                "Transition Projects (TPI) Housing - Clark Annex GPD - SP(4259)",
                "Transition Projects (TPI) Housing - Barbara Maher Apartments PSH - SP(3018)"
            ],
            "res": [
                "Transition Projects (TPI) - Jean's Place L1 - SP(29)",
                "Transition Projects (TPI) - Clark Center - SP(25)",
                "Transition Projects (TPI) - Doreen's Place - SP(28)",
                "Transition Projects (TPI) - VA Grant Per Diem (inc. Doreen's Place GPD) - SP(3189)"
            ],
            "es": [
                "ZZ - Transition Projects (TPI) - Columbia Shelter (Do not use after 4/25/18)(5857)",
                "Transition Projects (TPI) - Sears Emergency Shelter - SP(5218)",
                "z-Transition Projects (TPI) - Peace Annex Emergency Shelter - SP(5434)",
                "Transition Projects (TPI) - Peace 2(5793)",
                "Transition Projects (TPI) - Hansen Emergency Shelter - SP(5588)",
                "Transition Projects (TPI) - SOS Shelter(2712)",
                "Transition Projects (TPI) - 5th Avenue Shelter(6281)",
                "z-Transition Projects (TPI) - Peace Emergency Shelter - SP(5239)",
                "Transition Projects (TPI) - Columbia Shelter(6527)",
                "Transition Projects (TPI) - Willamette Center(5764)",
                "Transition Projects (TPI) - WyEast Emergency Shelter(6612)"
            ],
            "emerg": [],
            "ment": [],
            "rent": [],
            "out": [
                "Transition Projects (TPI) - Outreach - SP(3782)",
                "Transition Projects (TPI) - Coordinated Housing Access Team (CHAT)(5965)",
                "Ticket Home - Served (OR-501)(5431)"
            ],
            "well": [
                "Transition Projects (TPI) - Health Navigation(6050)",
                "Transition Projects (TPI) - Wellness Access(6051)"
            ],
            "TicketHome": ["Ticket Home - Served (OR-501)(5431)"]
        }
        self.wa_referrals = [
            "Referral - A&D Support",
            "Referral - Dental Care",
            "Referral - Eye Care",
            "Referral - Medical Care",
            "Referral - Mental Health Care"
        ]

    def count_entered_into_provider(self,entries_df,shelter,dept,quarter_end,fiscal_year):
        """
        metric: 300 people provided with a TicketHome; 1300
        participants will have a safe place to sleep; 2795 participants will
        have a safe place to sleep

        used by: residential shelter, emergency shelter

        :param entries_df: a pandas dataframe created from the all
        entries.xls report generated by ART

        :param dept: a string

        :param quarter_end: a datetime.datetime object

        :return: a pandas data frame
        """
        # create a local copy of the entries_df with quarter and fiscal year
        # columns added
        data = QuarterAndFiscalYear(
            entries_df[
                entries_df["Entry Exit Provider Id"].str.contains(shelter)
            ],
            exit_date_fill_type="specify",
            exit_date_fill=quarter_end,
            fill_na=True
        ).create_fy_q_columns()


        # add quarter counter columns
        q_data = return_quarters(
            data.drop_duplicates(
                subset=["Client Uid", "Entry Exit Entry Date"]
            )
        )
        q1 = q_data.drop_duplicates(subset=["Client Uid", "Q1"])
        q2 = q_data.drop_duplicates(subset=["Client Uid", "Q2"])
        q3 = q_data.drop_duplicates(subset=["Client Uid", "Q3"])
        q4 = q_data.drop_duplicates(subset=["Client Uid", "Q4"])

        # create a pivot table based on quarters
        pivot = pd.DataFrame.from_dict(
            {
                "Q1": [q1["Q1"].sum()],
                "Q2": [q2["Q2"].sum()],
                "Q3": [q3["Q3"].sum()],
                "Q4": [q4["Q4"].sum()]
            }
        )

        # add fytd column
        pivot["FYTD"] = len(
            q_data.drop_duplicates(subset="Client Uid").index
        )

        # add metric and goal columns that a dependent on the dept param
        if dept == "res":
            pivot["Metric"] = "1300 participants will have a safe place to sleep"
            pivot["Goal"] = 1300

            # return the pivot table
            return pivot

        else:
            pivot["Metric"] = "2795 participants will have a safe place to sleep"
            pivot["Goal"] = 2795

            # return the pivot table
            return pivot

    def count_exclusions_by_provider(self,exclusions_df,dept,next_quarter_end,shelter):
        """
        note: Currently this method only returns a count.  This will need to be
        altered so that a comparision is occuring to truely reflect the 15%
        decrease

        metric: There will be a 15% decrease in exclusions from shelters

        used by: Emergency Shelters

        :param exclusions_df: a panadas dataframe from the exclusions from
        provider.xls art report

        :param dept: a string representing the shortened department name. This
        string must be in the self.departments dict's keys

        :return:
        """
        # create a local copy of the exclusion data with columns for quarter
        # and fiscal year
        exclusions = QuarterAndFiscalYear(
            exclusions_df[
                exclusions_df["Infraction Provider"].str.contains(shelter) &
                exclusions_df["Infraction Banned Code"].notna() &
                (exclusions_df["Infraction Banned Code"] != "Warning") &
                (exclusions_df["Infraction Banned Code"] != "Safety Alert") &
                (exclusions_df["Infraction Banned Code"] != "Other")
            ][[
                "Client Uid",
                "Infraction Provider",
                "Infraction Banned Start Date",
                "Infraction Banned End Date",
                "Infraction Banned Code",
                "Infraction Type"
            ]],
            "specify",
            next_quarter_end,
            fill_na=True
        ).create_fy_q_columns()

        # create a pivot table of the quarter data
        pivot = pd.pivot_table(
            exclusions[
                (
                    exclusions["Infraction Banned End Date"] - exclusions["Infraction Banned Start Date"]
                ).dt.days > 30
            ],
            index="Infraction Banned Start Date Fiscal Year",
            columns="Infraction Banned Start Date Quarter",
            values="Client Uid",
            aggfunc=len
        )

        # add fytd, metric, and goal columns to the pivot tables
        pivot["FYTD"] = len(
            exclusions[
                (
                    exclusions["Infraction Banned End Date"] - exclusions["Infraction Banned Start Date"]
                ).dt.days > 30
            ].index)
        pivot["Metric"] = "There will be a 15% decrease in exclusions from shelters"
        pivot["Goal"] = "15%"

        # return the pivot table
        return pivot

    def percent_w_ss_service(self,entries_df,services_df,quarter_end,fiscal_year,dept,shelter):
        """
        metric: 50% of participants enrolled in our retention program will
        engage in supportive services; 75% of guests will connect to a supportive
        service; 75% of guests will connect to a supportive service

        used by:Residential Shelter, Emergency Shelter

        :param entries_df: a pandas data frame from the All Entries ART report

        :param services_df: a pandas data frame from the All Services ART report

        :param quarter_end: a datetime.datetime object
        """

        # a list of all the providers used by the supportive services department
        ss_dept = [
            "Transition Projects (TPI) - Support Services(4325)",
            "Transition Projects (TPI) - Wellness Access(6051)",
            "Transition Projects (TPI) - Health Navigation(6050)",
            "Transition Projects (TPI) - Substance Abuse Programming (IAP) - SP(3168)",
            "Transition Projects (TPI) - Substance Abuse Programming (PIAP) - SP(6074)",
            "Transition Projects (TPI) - Support Services - Employment(6593)",
            "Transition Projects (TPI) - Outreach - SP(3782)",
            "Transition Projects (TPI) - Health Connections - SERVICES ONLY(6481)",
            "Transition Projects (TPI) - Coordinated Housing Access Team (CHAT)(5965)"
        ]

        # create local copies of both data frames filling nan exit dates with
        # the last day in the current quarter, running the data through the
        # determine period script, and only returning data for participants with
        # an entry into Retention CM
        entries = QuarterAndFiscalYear(
            entries_df[
                entries_df["Entry Exit Provider Id"].str.contains(shelter)
            ],
            "specify",
            quarter_end,
            True
        ).create_fy_q_columns()

        # return a services df with fy and quarter columns matching department
        # spec
        if dept == "ret":
            services = QuarterAndFiscalYear(
                services_df[
                    services_df["Client Uid"].isin(entries["Client Uid"]) &
                    services_df["Service Provide Provider"].isin(ss_dept)
                ],
                fill_na=False
            ).create_fy_q_columns()
        else:
            services = QuarterAndFiscalYear(
                services_df[
                    services_df["Client Uid"].isin(entries["Client Uid"]) &
                    ~(services_df["Service Provide Provider"].isin(self.departments["res"])) &
                    ~(services_df["Service Provide Provider"].isin(self.departments["rec"])) &
                    ~(services_df["Service Provide Provider"].isin(self.departments["es"]))
                ],
                fill_na=False
            ).create_fy_q_columns()


        # merge the date columns from the entry data frame with the services
        # data
        merged_dfs = services.merge(
            entries[[
                "Client Uid",
                "Entry Exit Provider Id",
                "Entry Exit Entry Date",
                "Entry Exit Entry Date Fiscal Year",
                "Entry Exit Entry Date Quarter",
                "Entry Exit Exit Date",
                "Entry Exit Exit Date Fiscal Year",
                "Entry Exit Exit Date Quarter"
            ]],
            on="Client Uid",
            how="outer"
        )

        # filter for only rows where the service date is between the entry and
        # exit dates
        cleaned = merged_dfs[
            merged_dfs["Service Provide Start Date"].notna() &
            (
                (
                    (merged_dfs["Service Provide Start Date"] > merged_dfs["Entry Exit Entry Date"]) &
                    (merged_dfs["Service Provide Start Date"] < merged_dfs["Entry Exit Exit Date"])
                ) |
                (merged_dfs["Service Provide Start Date"].dt.date == merged_dfs["Entry Exit Entry Date"].dt.date) |
                (merged_dfs["Service Provide Start Date"].dt.date == merged_dfs["Entry Exit Exit Date"].dt.date)
            ) &
            (merged_dfs["Service Provide Start Date Fiscal Year"] == fiscal_year)
        ]

        # create a pivot table based on quarter showing unique participants with
        # a service during said quarter
        # to break out by provider simply change the index to be Entry Exit
        # Provider Id
        served = pd.pivot_table(
            cleaned.drop_duplicates(subset=[
                "Client Uid",
                "Service Provide Start Date Quarter"
            ]),
            index="Service Provide Start Date Fiscal Year",
            columns="Service Provide Start Date Quarter",
            values="Client Uid",
            aggfunc=len
        )

        # add a fytd column to the served df
        served["FYTD"] = len(
            cleaned.drop_duplicates(subset="Client Uid").index
        )
        # uncomment the next row to create the numerators of the per dept numbers
        # return served

        # use the np.select method to add Q1, Q2, Q3, Q4 columns for tracking if
        # an entry is active during a given quarter
        q_check = return_quarters(
            entries.drop_duplicates(subset=["Client Uid", "Entry Exit Entry Date Quarter"])
        )
        q1 = q_check.drop_duplicates(subset=["Client Uid", "Q1"])
        q2 = q_check.drop_duplicates(subset=["Client Uid", "Q2"])
        q3 = q_check.drop_duplicates(subset=["Client Uid", "Q3"])
        q4 = q_check.drop_duplicates(subset=["Client Uid", "Q4"])

        # create a pivot table for all participants with an open entry during a
        # given quarter
        all_pivot_dict = {
            "Q1": [q1["Q1"].sum()],
            "Q2": [q2["Q2"].sum()],
            "Q3": [q3["Q3"].sum()],
            "Q4": [q4["Q4"].sum()]
        }
        all_pivot = pd.DataFrame.from_dict(all_pivot_dict)

        # create a pivot table for all participants with an open entry during a
        # given fiscal year
        all_pivot["FYTD"] = len(entries.drop_duplicates(subset="Client Uid").index)

        # concatenate the two merged pivot tables
        concatenated = pd.concat([served, all_pivot], ignore_index=True).fillna(0)

        # add a % of participants served by support services row
        concatenated.loc["% of Participants Served by Support Services"] = (
            100*(concatenated.loc[0] / concatenated.loc[1])
        ).round(2)

        if dept == "retention":
            # add the metrics and goals columns
            concatenated["Metric"] = "50% of participants enrolled in our retention program will engage in supportive services"
            concatenated["Goal"] = "50%"
        elif dept == "res":
            concatenated["Metric"] = "75% of guests will connect to a supportive service"
            concatenated["Goal"] = "75%"
        else:
            concatenated["Metric"] = "50% of guests will connect to a supportive service"
            concatenated["Goal"] = "50%"

        # return the new pivot table
        return concatenated

    def percent_w_vi_spdat(self, entries_df, spdat_df, dept, shelter, quarter_end):
        """
        metric: 75%  of guests will be assessed for Coordinated Access

        used by: Residential Shetlers, Emergency Shelters

        :param entries_df: a pandas dataframe created from the All Entries.xls
        ART report

        :param services_df: a pandas dataframe created from the All Services.xls
        ART report

        :param dept: a string short version of the department name

        :return: a pandas dataframe
        """

        # create a list of client uids from spdat_df
        spdat = spdat_df[["Client Uid"]]

        # add quarter and fiscal year columns to a local copy of the entries_df
        # to break this report out by shelters simply replace the .isin statement
        # with a .str.contains(dept) statement and run per department
        entries = QuarterAndFiscalYear(
            entries_df[
                entries_df["Entry Exit Provider Id"].str.contains(shelter)
            ],
            "specify",
            quarter_end,
            True
        ).create_fy_q_columns()

        # use the return_quarters function to create a dataframe of participants
        # with an entry and a vi-spdat by quarter
        q_spdated = return_quarters(
            entries[entries["Client Uid"].isin(spdat["Client Uid"])]
        ).drop_duplicates(subset=["Client Uid", "Entry Exit Entry Date"])
        q1 = q_spdated.drop_duplicates(subset=["Client Uid", "Q1"])
        q2 = q_spdated.drop_duplicates(subset=["Client Uid", "Q2"])
        q3 = q_spdated.drop_duplicates(subset=["Client Uid", "Q3"])
        q4 = q_spdated.drop_duplicates(subset=["Client Uid", "Q4"])

        # create a pivot table from the q_spdated dataframe
        all_spdated_dict = {
            "Q1": [q1["Q1"].sum()],
            "Q2": [q2["Q2"].sum()],
            "Q3": [q3["Q3"].sum()],
            "Q4": [q4["Q4"].sum()]
        }
        all_spdated = pd.DataFrame.from_dict(all_spdated_dict)
        all_spdated["FYTD"] = len(entries[entries["Client Uid"].isin(spdat)].drop_duplicates(subset="Client Uid").index)

        # use the return_quarters function to create a dataframe of all participants
        # with a provider entry
        q_all = return_quarters(entries).drop_duplicates(subset=["Client Uid", "Entry Exit Entry Date"])
        q1 = q_all.drop_duplicates(subset=["Client Uid", "Q1"])
        q2 = q_all.drop_duplicates(subset=["Client Uid", "Q2"])
        q3 = q_all.drop_duplicates(subset=["Client Uid", "Q3"])
        q4 = q_all.drop_duplicates(subset=["Client Uid", "Q4"])

        # create a pivot table from the q_all dataframe
        all_dict = {
            "Q1": [q1["Q1"].sum()],
            "Q2": [q2["Q2"].sum()],
            "Q3": [q3["Q3"].sum()],
            "Q4": [q4["Q4"].sum()]
        }
        all_pivot = pd.DataFrame.from_dict(all_dict)
        all_pivot["FYTD"] = len(entries.drop_duplicates(subset="Client Uid").index)

        # create a % dataframe by dividing the other two
        percent = ((100*(all_spdated / all_pivot)).round(2)).fillna(0.0)

        # concatenate the data frames
        concatenated = pd.concat(
            [all_spdated, all_pivot, percent],
            ignore_index=True
        )

        # add metric and goal columns
        concatenated["Metric"] = "75%  of guests will be assessed for Coordinated Access"
        concatenated["Goal"] = "75%"

        # return the data concatendated data frame
        return concatenated

    def percent_entries_poc(self, entries_df, dept, quarter_end, shelter):
        """
        metric: 41% of participants served will be people of color

        used by: Residential Shelters, Emergency shelters

        :param entries_df: a pandas dataframe created from the all_entries + UDE
        ART report

        :return: a pandas dataframe
        """
        # create the poc list
        poc = CreatePOCList(entries_df).return_poc_list()

        # add quarter and fiscal year columns to a local copy of the data frame
        # then also add the columns identifying if a participant was enrolled
        # during a given quarter
        # to break out by provider replace .isin() statement with .str.contains()
        # statement and run per provider
        data = return_quarters(
            QuarterAndFiscalYear(
                entries_df[
                    entries_df["Entry Exit Provider Id"].str.contains(shelter)
                ],
                "specify",
                quarter_end,
                fill_na=True
            ).create_fy_q_columns()
        )

        # create a poc version of the DataFrame
        poc_data = data[
            data["Client Uid"].isin(poc)
        ][["Client Uid", "Q1", "Q2", "Q3", "Q4"]]
        pocq1 = poc_data.drop_duplicates(subset=["Client Uid", "Q1"])
        pocq2 = poc_data.drop_duplicates(subset=["Client Uid", "Q2"])
        pocq3 = poc_data.drop_duplicates(subset=["Client Uid", "Q3"])
        pocq4 = poc_data.drop_duplicates(subset=["Client Uid", "Q4"])

        # create a dataframe that will show sums of unique participants per quarters
        cleaned = data[
            ["Client Uid", "Q1", "Q2", "Q3", "Q4"]
        ]
        q1 = cleaned.drop_duplicates(subset=["Client Uid", "Q1"])
        q2 = cleaned.drop_duplicates(subset=["Client Uid", "Q2"])
        q3 = cleaned.drop_duplicates(subset=["Client Uid", "Q3"])
        q4 = cleaned.drop_duplicates(subset=["Client Uid", "Q4"])

        q_data = pd.DataFrame.from_dict(
            {
                "Q1": [q1["Q1"].sum()],
                "Q2": [q2["Q2"].sum()],
                "Q3": [q3["Q3"].sum()],
                "Q4": [q4["Q4"].sum()]
            }
        )

        # add a FYTD column
        q_data["FYTD"] = len(cleaned.drop_duplicates(subset="Client Uid").index)

        # create poc quarter data
        poc_q_data = pd.DataFrame.from_dict(
            {
                "Q1": [pocq1["Q1"].sum()],
                "Q2": [pocq2["Q2"].sum()],
                "Q3": [pocq3["Q3"].sum()],
                "Q4": [pocq4["Q4"].sum()]
            }
        )

        # add a FYTD column to the poc_q_data
        poc_q_data["FYTD"] = len(poc_data.drop_duplicates(subset="Client Uid").index)

        # create a percent dataframe
        percent = (100*(poc_q_data / q_data)).round(2)

        # add metric and goals columns
        percent["Metric"] = "41% of participants served will be people of color"
        percent["Goal"] = "41%"

        # concatenate the three dataframes
        concatenated = pd.concat([poc_q_data, q_data, percent], ignore_index=True)

        # return the concatenated dataframe
        return concatenated

if __name__ == "__main__":
    shelters = [
        ("Doreen", "res"),
        ("Clark Center", "res"),
        ("Jean", "res"),
        ("Columbia", "es"),
        ("SOS", "es"),
        ("Willamette", "es"),
        ("WyEast", "es")
    ]
    entries = pd.read_excel(askopenfilename(title="Entries"))
    services = pd.read_excel(askopenfilename(title="Services"))
    spdat = pd.read_excel(askopenfilename(title="SPDAT"))
    exclusions = pd.read_excel(askopenfilename(title="Exclusions"))
    quarter_end = datetime(year=2018, month=9, day=30)
    fiscal_year = "FY 18-19"
    next_quarter_end = datetime(year=2018, month=12, day=31)
    af = AllFunctions()
    writer = pd.ExcelWriter(asksaveasfilename(title="Save"), engine="xlsxwriter")

    for shelter, dept in shelters:
        m1 = af.count_entered_into_provider(entries, shelter, dept, quarter_end, fiscal_year)
        m2 = af.percent_w_ss_service(entries, services, quarter_end, fiscal_year, dept, shelter)
        m3 = af.percent_w_vi_spdat(entries, spdat, dept, shelter, quarter_end)
        m4 = af.percent_entries_poc(entries, dept, quarter_end, shelter)
        m5 = af.count_exclusions_by_provider(exclusions, dept, next_quarter_end, shelter)


        pd.concat([m1, m2, m3, m4, m5], ignore_index=True).to_excel(writer, sheet_name=shelter, index=False)

    writer.save()
