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


    def count_entered_into_provider(self, entries_df, dept, quarter_end, fiscal_year):
        """
        metric: 300 people provided with a TicketHome; 1300
        participants will have a safe place to sleep; 2795 participants will
        have a safe place to sleep

        used by: Outreach, residential shelter, emergency shelter

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
                entries_df["Entry Exit Provider Id"].isin(
                    self.departments[dept]
                )
            ],
            exit_date_fill_type="specify",
            exit_date_fill=quarter_end,
            fill_na=True
        ).create_fy_q_columns()

        # check what department this call is for and act accordinly
        if dept == "TicketHome":
            # create a pivot table based on unique participants per quarter
            pivot = pd.pivot_table(
                data[
                    data["Entry Exit Entry Date Fiscal Year"] == fiscal_year
                ].drop_duplicates(
                    subset=["Client Uid", "Entry Exit Entry Date Quarter"]
                ),
                index="Entry Exit Entry Date Fiscal Year",
                columns="Entry Exit Entry Date Quarter",
                values="Client Uid",
                aggfunc=len
            )

            # add a fiscal year column
            pivot["FYTD"] = len(
                data[
                    data["Entry Exit Entry Date Fiscal Year"] == fiscal_year
                ].drop_duplicates(subset="Client Uid").index
            )

            # add goal and metric columns
            pivot["Metric"] = "300 people provided with a ticket home"
            pivot["Goal"] = 300

            # return the pivot table
            return pivot

        elif (dept == "res") or (dept == "es"):
            # add quarter counter columns
            q_data = return_quarters(
                data.drop_duplicates(
                    subset=["Client Uid"]
                )
            )

            # create a pivot table based on quarters
            pivot = pd.DataFrame.from_dict(
                {
                    "Q1": [q_data["Q1"].sum()],
                    "Q2": [q_data["Q2"].sum()],
                    "Q3": [q_data["Q3"].sum()],
                    "Q4": [q_data["Q4"].sum()]
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

        else:
            pass


    def count_exclusions_by_provider(self, exclusions_df, dept, next_quarter_end):
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
                exclusions_df["Infraction Provider"].isin(self.departments[dept]) &
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


    def count_placed_into_perm(self, placements_df, dept):
        """
        metric: 1,200 people will obtain permanent housing; 750 people will
        obtain housing; 450 veteran families will obtain housing

        used by: agency, housing cm, veterans

        :param placements_df: a pandas pivot table generated from the placements
        v.4.0 + HH.xls Art report

        :param dept: a string from the following list agency, housing

        :return: a pandas pivot table
        """
        # Add the FY and Quarter columns to the data set dropping rows with a
        # null intervention type after checking to see what department is
        # calling the function and returning the appropriate data set
        if dept.lower() == "agency":
            data = QuarterAndFiscalYear(
                placements_df,
                fill_na=False
            ).create_fy_q_columns().dropna(subset=["Intervention Type (TPI)(8745)"])
        elif dept.lower() == "housing":
            data = QuarterAndFiscalYear(
                placements_df[
                    (
                        (placements_df["Department Placed From(3076)"] == "ACCESS") &
                        ~(placements_df["Reporting Program (TPI)(8748)"] == "Ticket Home - Served")
                    ) |
                    (placements_df["Department Placed From(3076)"] == "Residential CM")
                ],
                fill_na=False
            ).create_fy_q_columns().dropna(subset=["Intervention Type (TPI)(8745)"])
        elif dept.lower() == "vets":
            data = QuarterAndFiscalYear(
                placements_df[
                    (placements_df["Department Placed From(3076)"].str.contains("SSVF"))
                ],
                fill_na=False
            ).create_fy_q_columns().dropna(subset=["Intervention Type (TPI)(8745)"])
        else:
            print("Error: Dept Parameter Invalid. {} must be in param list".format(dept))

        if (dept == "housing") | (dept == "agency"):
            # Create a pivot table for the quarters droping duplicate placements
            # using client uid, fiscal year, and fiscal quarter
            q_perm_placements = pd.pivot_table(
                data[
                    data[
                        "Intervention Type (TPI)(8745)"
                    ].str.contains("Permanent")
                ].drop_duplicates(
                    subset=[
                        "Client Uid",
                        "Placement Date(3072) Fiscal Year",
                        "Placement Date(3072) Quarter"
                    ]
                ),
                index=["Placement Date(3072) Fiscal Year"],
                columns=["Placement Date(3072) Quarter"],
                values="Client Uid",
                aggfunc=len
            )

            # Creat a pivot table for the fiscal years dropping duplicate placements
            # using client uid and fiscal year
            y_perm_placements = pd.pivot_table(
                data[
                    data[
                        "Intervention Type (TPI)(8745)"
                    ].str.contains("Permanent")
                ].drop_duplicates(
                        subset=[
                            "Client Uid",
                            "Placement Date(3072) Fiscal Year"
                        ]
                    ),
                index="Placement Date(3072) Fiscal Year",
                values="Client Uid",
                aggfunc=len
            )

            # Merge the two pivot tables, dropping the index name to make them more
            # readable and to make them more easily printable
            merged = q_perm_placements.merge(
                y_perm_placements,
                left_index=True,
                right_index=True,
                how="outer"
            ).rename_axis(None).rename(
                columns={"Client Uid": "FYTD"}
            )
        elif dept == "vets":
            # Create a pivot table for the quarters droping duplicate placements
            # using client uid, fiscal year, and fiscal quarter
            merged = pd.pivot_table(
                data[
                    data[
                        "Intervention Type (TPI)(8745)"
                    ].str.contains("Permanent")
                ].drop_duplicates(
                    subset=[
                        "Household Uid"
                        ]
                ).drop_duplicates(
                    subset=["Client Uid"]
                ),
                index="Placement Date(3072) Fiscal Year",
                columns="Placement Date(3072) Quarter",
                values="Household Uid",
                aggfunc=len
            )

            # Creat a fytd total column
            merged["FYTD"] = len(
                data[
                    data["Intervention Type (TPI)(8745)"].str.contains("Permanent")
                ].drop_duplicates(subset="Household Uid").index
            )


        # Add the department and metric columns pre-filled with the appropriate
        # values
        if dept == "agency":
            merged["Goal"] = 1200
            merged["Metric"] = "1,200 people will obtain permanent housing"
        elif dept == "housing":
            merged["Goal"] = 750
            merged["Metric"] = "750 People Will Obtain Housing"
        elif dept == "vets":
            merged["Goal"] = 450
            merged["Metric"] = "450 Veteran Families Will Obtain Housing"

        return merged


    def count_placed_into_ep(self, placements_df):
        """
        metric: 60 veteran families will have evictions prevented

        used by: Veterans

        :param placements_df: a pandas data frame from the placements v.4 + HH

        :return: a pandas DataFrame
        """
        # Add the quarter and fiscal year columns
        data = QuarterAndFiscalYear(
            placements_df[
                (placements_df["Intervention Type (TPI)(8745)"] == "Eviction Prevention") &
                (placements_df["Department Placed From(3076)"].str.contains("SSVF"))
            ],
            fill_na=False
        ).create_fy_q_columns()

        # create the pivot table
        pivot = pd.pivot_table(
            data.drop_duplicates(subset=["Household Uid", "Placement Date(3072) Quarter"]),
            columns="Placement Date(3072) Quarter",
            values="Household Uid",
            aggfunc=len
        )
        pivot["FYTD"] = len(data.drop_duplicates(subset="Household Uid").index)

        # Add the metric and goal columns
        pivot["Metric"] = "60 veteran families will have evictions prevented"
        pivot["Goal"] = 60

        # Return the pivot table
        return pivot


    def count_referred_to_h_w_service(self, services_df):
        """
        metric: 800 people will be referred to health and wellness services

        used by: health and wellness

        :param services_df: a pandas data frame from the all services + need
        status.xls art report

        :return:
        """
        # add quarter and fiscaly year data to a local copy of services data
        data = QuarterAndFiscalYear(
            services_df[
                services_df["Service Provide Provider"].isin(self.departments["well"]) &
                services_df["Service Provider Specific Code"].isin(self.wa_referrals)
            ],
            fill_na=False
        ).create_fy_q_columns()

        # create a pivot table based on quarters
        pivot = pd.pivot_table(
            data.drop_duplicates(
                subset=["Client Uid", "Service Provide Start Date Quarter"]
            ),
            index="Service Provide Start Date Fiscal Year",
            columns="Service Provide Start Date Quarter",
            values="Client Uid",
            aggfunc=len
        )


        # add fytd, metric, and goal columns
        pivot["FYTD"] = len(data.drop_duplicates(subset="Client Uid").index)
        pivot["Metric"] = "800 people will be referred to health and wellness services"
        pivot["Goal"] = 800

        # return the pivot table
        return pivot


    def count_attend_rent_well(self, services_df):
        """
        metric: 400 Transition Projects participats will enroll in RentWell

        used by: RentWell

        :param services_df: a pandas data frame

        :return: a pandas data frame
        """
        # add quarter and fiscal year values to a local copy of the services_df
        data = QuarterAndFiscalYear(
            services_df[
                services_df["Service Provider Specific Code"].notna() &
                services_df["Service Provider Specific Code"].str.contains("RentWell")
            ].drop_duplicates(subset=["Client Uid", "Service Provide Start Date"]),
            fill_na=False
        ).create_fy_q_columns()

        # create a pivot table showing participant count by quarter
        pivot = pd.pivot_table(
            data.drop_duplicates(subset=["Client Uid", "Service Provide Start Date Quarter"]),
            index="Service Provide Start Date Fiscal Year",
            columns="Service Provide Start Date Quarter",
            values="Client Uid",
            aggfunc=len
        )

        # add a fytd column
        pivot["FYTD"] = len(data.drop_duplicates(subset="Client Uid").index)

        # add metric and goal columns
        pivot["Metric"] = "400 Transition Projects participats will enroll in RentWell"
        pivot["Goal"] = 400

        # return the pivot table
        return pivot


    def count_document_ready(self, spdat_df):
        """
        metric: 60 individuals waiting for PSH get application-ready

        goal: 60

        :param spdat_df: a panadas dataframe

        :return: a pandas dataframe
        """

        # create a local copy of the spdat_df with quarter and fiscal year columns
        data = QuarterAndFiscalYear(
            spdat_df.dropna(subset=["Date Document Ready - ALL Top Priority Documents are COMPLETE (Only Answer Once)(9572)"])
        ).create_fy_q_columns()

        # create a pivot table
        pivot = pd.pivot_table(
            data.drop_duplicates(subset="Client Uid"),
            index="Date Document Ready - ALL Top Priority Documents are COMPLETE (Only Answer Once)(9572) Fiscal Year",
            columns="Date Document Ready - ALL Top Priority Documents are COMPLETE (Only Answer Once)(9572) Quarter",
            values="Client Uid",
            aggfunc=len
        )

        # create FYTD, Metric, and Goal columns
        pivot["FYTD"] = len(data.drop_duplicates(subset="Client Uid"))
        pivot["Metric"] = "60 individuals waiting for PSH get application-ready"
        pivot["Goal"] = 60

        # return the relevant data
        return pivot


    def count_served_by_provider(self, services_df, dept):
        """
        metric: 8500 people will be served by the resource center

        used by: resource center

        :param services_df: a pandas data frame created from the all services
        (all agency).xlsx report from ART

        :param dept: the short name of the department

        :return:
        """
        # add quarter and fiscal year columns to a local copy of the data frame
        data = QuarterAndFiscalYear(
            services_df[
                services_df["Service Provide Provider"].isin(self.departments[dept])
            ].drop_duplicates(subset=["Client Uid", "Service Provide Start Date"]),
            fill_na=False
        ).create_fy_q_columns()

        # create a pivot table deduplicated by quarter
        pivot = pd.pivot_table(
            data.drop_duplicates(subset=[
                "Client Uid",
                "Service Provide Start Date Quarter"
            ]),
            index="Service Provide Start Date Fiscal Year",
            columns="Service Provide Start Date Quarter",
            values="Client Uid",
            aggfunc=len
        )

        # add fytd, metric, and goal columns
        pivot["FYTD"] = len(data.drop_duplicates(subset="Client Uid").index)
        pivot["Metric"] = "8500 people will be served by the Resource Center"
        pivot["Goal"] = 8500

        # return the pivot table
        return pivot


    def count_served_with_hygiene_services(self, services_df, dept):
        """
        metric: 40,000 hygiene services will be provided

        used by: resource center

        :param services_df: a pandas data frame created from the all services
        (all tpi).xls ART report

        :param dept: a string of the shortened department name

        :return: a pivot table
        """
        # a list of service provider specific codes to by tracked
        hygiene_services = [
            "Hairdressing/Nail Care",
            "Laundry Supplies",
            "Personal Grooming Supplies",
            "Showers"
        ]

        # add quarter and fiscal years to a local copy of the services DataFrame
        # showing only services in the hygiene_services list
        data = QuarterAndFiscalYear(
            services_df[
                services_df["Service Provide Provider"].isin(self.departments[dept]) &
                services_df["Service Provider Specific Code"].isin(hygiene_services)
            ],
            fill_na=False
        ).create_fy_q_columns()

        # create a pivot table by quarter
        pivot = pd.pivot_table(
            data,
            index="Service Provide Start Date Fiscal Year",
            columns="Service Provide Start Date Quarter",
            values="Client Uid",
            aggfunc=len
        )

        # add fytd, metric, and goal columns to the pivot table
        pivot["FYTD"] = len(data.index)
        pivot["Metric"] = "40,000 hygiene services will be provided"
        pivot["Goal"] = "40,000"

        # return the pivot table
        return pivot


    def count_spdated(self, spdat_df):
        """
        metric: Complete 500 assesments for permanent supportive housing

        goal: 500

        :param spdat_df: a pandas dataframe created from the VI-SPDAT Report v0.2

        :return: a pandas dataframe
        """
        # add fiscal year and quarter columns to a local copy of the dataframe
        data = QuarterAndFiscalYear(
            spdat_df[["Client Uid", "Date Added (7144-date_added)"]].dropna(
                subset=["Date Added (7144-date_added)"]
            ).drop_duplicates(subset="Client Uid"),
            fill_na=False
        ).create_fy_q_columns()

        # create a pivot table
        pivot = pd.pivot_table(
            data,
            index="Date Added (7144-date_added) Fiscal Year",
            columns="Date Added (7144-date_added) Quarter",
            values="Client Uid",
            aggfunc=len
        )

        # add FYTD, Metric an Goal columns
        pivot["FYTD"] = len(data.index)
        pivot["Metric"] = "Complete 500 assesments for permanent supportive housing"
        pivot["Goal"] = 500

        # return the pivot table
        return pivot


    def percent_agency_poc(self, entry_df, services_df):
        """
        metric: 41% of participants served will be people of color

        used by: Agency

        :param entriy_df:

        :services_df:

        :return:
        """
        # add quarter columns to the entry data
        shelter_stays = return_quarters(
            entry_df[
                entry_df["Entry Exit Provider Id"].isin(self.departments["res"]) |
                entry_df["Entry Exit Provider Id"].isin(self.departments["es"]) |
                entry_df["Entry Exit Provider Id"].isin(self.departments["ca bm"])
            ]
        )

        # add quarter values to the services data
        q_services = QuarterAndFiscalYear(services_df, fill_na=False).create_fy_q_columns()

        merge = shelter_stays[shelter_stays["Q1"] == 1].merge(
            q_services[q_services["Service Provide Start Date Quarter"] == "Q1"],
            on=[
                "Client Uid",
                "Race(895)",
                "Race-Additional(1213)",
                "Ethnicity (Hispanic/Latino)(896)"
            ],
            how="outer"
        ).drop_duplicates(subset="Client Uid")
        merge_2 = shelter_stays[shelter_stays["Q2"] == 1].merge(
            q_services[q_services["Service Provide Start Date Quarter"] == "Q2"],
            on=[
                "Client Uid",
                "Race(895)",
                "Race-Additional(1213)",
                "Ethnicity (Hispanic/Latino)(896)"
            ],
            how="outer"
        ).drop_duplicates(subset="Client Uid")
        merge_3 = shelter_stays[shelter_stays["Q3"] == 1].merge(
            q_services[q_services["Service Provide Start Date Quarter"] == "Q3"],
            on=[
                "Client Uid",
                "Race(895)",
                "Race-Additional(1213)",
                "Ethnicity (Hispanic/Latino)(896)"
            ],
            how="outer"
        ).drop_duplicates(subset="Client Uid")
        merge_4 = shelter_stays[shelter_stays["Q2"] == 1].merge(
            q_services[q_services["Service Provide Start Date Quarter"] == "Q4"],
            on=[
                "Client Uid",
                "Race(895)",
                "Race-Additional(1213)",
                "Ethnicity (Hispanic/Latino)(896)"
            ],
            how="outer"
        ).drop_duplicates(subset="Client Uid")

        # create the output dataframe
        output = pd.DataFrame.from_dict(
            {
                "Q1": [
                    len(CreatePOCList(merge).return_poc_list()),
                    len(merge.index)
                ],
                "Q2": [
                    len(CreatePOCList(merge_2).return_poc_list()),
                    len(merge_2.index)
                ],
                "Q3": [
                    len(CreatePOCList(merge_3).return_poc_list()),
                    len(merge_3.index)
                ],
                "Q4": [
                    len(CreatePOCList(merge_4).return_poc_list()),
                    len(merge_4.index)
                ]
            }
        )

        # add the % row
        output.loc[3] = (100*(output.loc[0]/output.loc[1])).round(2)

        # add the metric and goals columns
        output["Metric"] = "41% of participants served will be people of color"
        output["Goal"] = "41%"

        # return the final dataframe
        return output


    def percent_day_hf_ss(self, services_df, quarter_starts):
        """
        metric: 50% of participants will connect to a housing-focused supportive
        service

        request: Create a report that allows us to count participants who have a
        service in the resource center then, later, during the same fiscal year,
        gets a service from another part of the agency that is not a shelter
        provider.

        used by: recource center

        Methodology:
        Pull in services as a pandas dataframe

        Look for each participant's first service from the resource center in a
        given fiscal year and make this into a dataframe

        Make a dataframe from the services data that doesn't include any services
        from the resource center or the shelters

        Merge the new dataframe with the resource center df using a left merge
        and the resouce center data as the right element on the client id

        Drop rows where the non-resource center service is prior to the the
        resource center service

        Sort by date and drop duplicates keeping the oldest

        Count by FYTD and return a % of total pt served during FYTD

        :param services_df: a pandas dataframe created from the All Services.xlsx
        ART report

        :param quarter_starts:a list of datetime.datetime objects containing
        only year, month, and day.  No smaller units should be present.
        """
        # define a dictionary for holding output values
        output_dict = {
            "Metric": [
                "50% of participants will connect to a housing-focused supportive service",
                "50% of participants will connect to a housing-focused supportive service",
                "50% of participants will connect to a housing-focused supportive service"
            ],
            "Goal": ["50%", "50%", "50%"],
            "Q1": [np.nan, np.nan, np.nan],
            "Q2": [np.nan, np.nan, np.nan],
            "Q3": [np.nan, np.nan, np.nan],
            "Q4": [np.nan, np.nan, np.nan],
            "FYTD": [np.nan, np.nan, np.nan]
        }

        # loop through the datestime values in the quarter_starts paramerter
        # creating quarter columns
        for date in quarter_starts:
            # slice the services_df so that it only contains services from the
            # resource center
            rec_df = services_df[
                services_df["Service Provide Provider"].isin(self.departments["rec"]) &
                (services_df["Service Provide Start Date"] < date)
            ].sort_values(
                by=["Client Uid", "Service Provide Start Date"],
                ascending=True
            ).drop_duplicates(subset=["Client Uid"], keep="first")

            # slice the services_df so that it only contains services from the
            # support services and case management departments
            other_df = services_df[
                ~(services_df["Service Provide Provider"].isin(self.departments["res"])) &
                ~(services_df["Service Provide Provider"].isin(self.departments["es"])) &
                ~(services_df["Service Provide Provider"].isin(self.departments["rec"])) &
                (services_df["Service Provide Start Date"] < date)
            ]

            # merge the two sliced data frames
            merged_df = other_df.merge(
                rec_df,
                how="left",
                on="Client Uid",
                suffixes=("_other", "_day")
            )

            # slice the merged_df so that it only includes service provide start
            # date_other is creater than the service provide start date_day value
            # this df will then have its rows sorted by the service_provide start
            # date_day column with values ascending.  Then the dataframe will be
            # de-duplicated by client uid and the service provide start Date_day
            # keeping the first unique value encourntered
            connected_df = merged_df[
                merged_df["Service Provide Start Date_other"] > merged_df["Service Provide Start Date_day"]
            ].sort_values(
                by=["Client Uid", "Service Provide Start Date_day"],
                ascending=True
            ).drop_duplicates(subset="Client Uid", keep="first")

            if date.month == 10:
                output_dict["Q1"] = [
                    len(connected_df.index),
                    len(rec_df.index),
                    (100*(len(connected_df.index)/len(rec_df.index)))
                ]
            elif date.month == 1:
                output_dict["Q2"] = [
                    len(connected_df.index),
                    len(rec_df.index),
                    (100*(num_connected/num_rec))
                ]
            elif date.month == 4:
                output_dict["Q3"] = [
                    len(connected_df.index),
                    len(rec_df.index),
                    (100*(num_connected/num_rec))
                ]
            else:
                output_dict["Q4"] = [
                    len(connected_df.index),
                    len(rec_df.index),
                    (100*(num_connected/num_rec))
                ]
                output_dict["FYTD"] = [
                    len(connected_df.index),
                    len(rec_df.index),
                    (100*(num_connected/num_rec))
                ]

        return pd.DataFrame.from_dict(output_dict).fillna(0)


    def percent_entries_poc(self, entries_df, dept, quarter_end):
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
                    entries_df["Entry Exit Provider Id"].isin(self.departments[dept])
                ],
                "specify",
                quarter_end,
                fill_na=True
            ).create_fy_q_columns()
        )

        # create a poc version of the DataFrame
        poc_data = data[data["Client Uid"].isin(poc)].drop_duplicates(subset=["Client Uid"])[["Q1", "Q2", "Q3", "Q4"]]

        # create a dataframe that will show sums of unique participants per quarters
        cleaned = data[["Client Uid", "Q1", "Q2", "Q3", "Q4"]].drop_duplicates(subset=["Client Uid"]).drop_duplicates(subset=["Client Uid", "Q1", "Q2", "Q3", "Q4"])
        q_data = pd.DataFrame.from_dict(
            {
                "Q1": [cleaned["Q1"].sum()],
                "Q2": [cleaned["Q2"].sum()],
                "Q3": [cleaned["Q3"].sum()],
                "Q4": [cleaned["Q4"].sum()]
            }
        )

        # add a FYTD column
        q_data["FYTD"] = len(cleaned.index)

        # create poc quarter data
        poc_q_data = pd.DataFrame.from_dict(
            {
                "Q1": [poc_data["Q1"].sum()],
                "Q2": [poc_data["Q2"].sum()],
                "Q3": [poc_data["Q3"].sum()],
                "Q4": [poc_data["Q4"].sum()]
            }
        )

        # add a FYTD column to the poc_q_data
        poc_q_data["FYTD"] = len(poc_data.index)

        # create a percent dataframe
        percent = (100*(poc_q_data / q_data)).round(2)

        # add metric and goals columns
        percent["Metric"] = "41% of participants served will be people of color"
        percent["Goal"] = "41%"

        # concatenate the three dataframes
        concatenated = pd.concat([poc_q_data, q_data, percent], ignore_index=True)

        # return the concatenated dataframe
        return concatenated


    def percent_exits_by_destination(self, entries_df, provider_type, dept):
        """
        Note: pos in the context of this method indicates positive
        metric: X% of people exiting our X selters will exit to
        permanent or stable housing

        used by: Agency, Housing CM, Permanent Housing (use dept of ca bm and a
        provider type of perm)

        :param entries_df:

        :param provider_type:

        :param dept: The department this metric relates to.  The must be a
        string included in the following list agency, housing

        :return:
        """
        data = entries_df

        # This function will be used for calculating the agency wide metrics
        def combined(data_frame, provider):
            if provider.lower() == "res":
                leavers = QuarterAndFiscalYear(
                    data[
                        data["Entry Exit Provider Id"].isin(
                            self.departments[provider_type.lower()]
                        ) &
                        data["Entry Exit Exit Date"].notna()
                    ],
                    fill_na=False
                ).create_fy_q_columns()

                # Create quarter and year pivot tables
                q_pos_pivot = pd.pivot_table(
                    leavers[
                        leavers["Entry Exit Destination"].isin(self.perm_dest) |
                        leavers["Entry Exit Destination"].isin(self.temp_dest)
                    ],
                    index="Entry Exit Exit Date Fiscal Year",
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_pos_pivot["FYTD"] = len(
                    leavers[
                        leavers["Entry Exit Destination"].isin(self.perm_dest) |
                        leavers["Entry Exit Destination"].isin(self.temp_dest)
                    ].index
                )

                q_pivot = pd.pivot_table(
                    leavers,
                    index="Entry Exit Exit Date Fiscal Year",
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_pivot["FYTD"] = len(
                    leavers.index
                )

                # create percent rows
                percent = (100*(q_pos_pivot / q_pivot)).round(2)

                concatenated = pd.concat(
                    [q_pos_pivot, q_pivot, percent],
                    ignore_index=True
                )

                # Add the metric and goal columns
                concatenated["Metric"] = "55% of people exiting our residential sheters will exit to permanent or stable housing"
                concatenated["Goal"] = "55%"

                # Return the results
                return concatenated

            elif provider.lower() == "es":
                leavers = QuarterAndFiscalYear(
                    data[
                        data["Entry Exit Provider Id"].isin(
                            self.departments[provider_type.lower()]
                        ) &
                        data["Entry Exit Exit Date"].notna()
                    ],
                    fill_na=False
                ).create_fy_q_columns()

                # Create quarter and year pivot tables
                q_pos_pivot = pd.pivot_table(
                    leavers[
                        leavers["Entry Exit Destination"].isin(self.perm_dest) |
                        leavers["Entry Exit Destination"].isin(self.temp_dest)
                    ],
                    index="Entry Exit Exit Date Fiscal Year",
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_pos_pivot["FYTD"] = len(
                    leavers[
                        leavers["Entry Exit Destination"].isin(self.perm_dest) |
                        leavers["Entry Exit Destination"].isin(self.temp_dest)
                    ].index
                )

                q_pivot = pd.pivot_table(
                    leavers,
                    index="Entry Exit Exit Date Fiscal Year",
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_pivot["FYTD"] = len(leavers.index)

                # merge the q_pivot and y_pivot pivot tables
                percent = (100*(q_pos_pivot / q_pivot)).round(2)

                concatenated = pd.concat(
                    [q_pos_pivot, q_pivot, percent],
                    ignore_index=True
                )

                # Add the metric and goal columns
                concatenated["Metric"] = "25% of people exiting our emergency sheters will exit to permanent or stable housing"
                concatenated["Goal"] = "25%"

                # Return the results
                return concatenated

            elif provider.lower() == "ca bm":
                leavers = QuarterAndFiscalYear(
                    data[
                        data["Entry Exit Provider Id"].isin(
                            self.departments[provider.lower()]
                        ) &
                        data["Entry Exit Exit Date"].notna()
                    ],
                    fill_na=False
                ).create_fy_q_columns()
                conds = [
                    leavers["Entry Exit Destination"].isin(self.perm_dest),
                    leavers["Entry Exit Destination"].isin(self.temp_dest)
                ]
                choices = ["Yes", "Yes"]
                leavers["Perm Stable"] = np.select(conds, choices, default="No")

                # Create quarter and year pivot tables
                q_pos_pivot = pd.pivot_table(
                    leavers[
                        (leavers["Perm Stable"] == "Yes")
                    ].drop_duplicates(
                        subset=[
                            "Client Uid",
                            "Entry Exit Exit Date Fiscal Year",
                            "Entry Exit Exit Date Quarter"
                        ]
                    ),
                    index="Entry Exit Exit Date Fiscal Year",
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_pos_pivot["FYTD"] = len(
                    leavers[
                        leavers["Perm Stable"] == "Yes"
                    ].drop_duplicates(
                        subset=[
                            "Client Uid",
                            "Entry Exit Exit Date Fiscal Year"
                        ]
                    ).index
                )

                q_pivot = pd.pivot_table(
                    leavers[
                         leavers["Entry Exit Exit Date"].notna()
                    ].drop_duplicates(
                        subset=[
                            "Client Uid",
                            "Entry Exit Exit Date Fiscal Year",
                            "Entry Exit Exit Date Quarter"
                        ]
                    ),
                    index="Entry Exit Exit Date Fiscal Year",
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_pivot["FYTD"] = len(
                    leavers[
                        leavers["Entry Exit Exit Date"].notna()
                    ].drop_duplicates(
                        subset=[
                            "Client Uid",
                            "Entry Exit Exit Date Fiscal Year"
                        ]
                    ).index
                )

                # create the percent dataframe
                percent = (100*(q_pos_pivot / q_pivot)).round(2)

                concatenated = pd.concat(
                    [q_pos_pivot, q_pivot, percent],
                    ignore_index=True
                )

                # Add the metric and goal columns
                concatenated["Metric"] = "75% of all exits from clark annex and barbara maher will be into permanent or stable housing"
                concatenated["Goal"] = "75%"

                # Return the results
                return concatenated

            else:
                pass

        # This function will be used for calculating the housing cm dept metrics
        def detail(data_frame, provider):
            #
            if provider.lower() == "res":
                # Add the quarter and fiscal year columns
                leavers = QuarterAndFiscalYear(
                    data[
                        data["Entry Exit Provider Id"].isin(
                            self.departments[provider_type.lower()]
                        ) &
                        data["Entry Exit Exit Date"].notna()
                    ],
                    fill_na=False
                ).create_fy_q_columns()
                conds = [
                    leavers["Entry Exit Destination"].isin(self.perm_dest),
                    leavers["Entry Exit Destination"].isin(self.temp_dest),
                    ~(
                        leavers["Entry Exit Destination"].isin(self.perm_dest) |
                        leavers["Entry Exit Destination"].isin(self.temp_dest)
                    )
                ]
                choices = ["Perm", "Stable", "Homeless"]
                leavers["Exit Destination"] = np.select(conds, choices, default="Homeless")

                # Create the pivot tables showing exit destination count by
                # quarter
                q_perm = pd.pivot_table(
                    leavers[
                        leavers["Entry Exit Destination"].isin(self.perm_dest)
                    ],
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_perm["FYTD"] = len(
                    leavers[
                        leavers["Entry Exit Destination"].isin(self.perm_dest)
                    ].index)

                q_stable = pd.pivot_table(
                    leavers[
                        leavers["Entry Exit Destination"].isin(self.temp_dest)
                    ],
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_stable["FYTD"] = len(
                    leavers[
                        leavers["Entry Exit Destination"].isin(self.temp_dest)
                    ].index)

                q_any = pd.pivot_table(
                    leavers,
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_any["FYTD"] = len(
                    leavers.index
                )

                # Create % columns
                percent_perm = (100*(q_perm / q_any)).round(2)
                percent_stab = (100*(q_stable / q_any)).round(2)

                # Concatenate the quarter based pivot tables into a single table
                concatenated = pd.concat(
                    [q_perm, q_stable, q_any, percent_perm, percent_stab],
                    ignore_index=True
                )

                # add metric and goal columns
                concatenated["Metric"] = [
                    "",
                    "",
                    "",
                    "35% of people exiting our residential shelters will exit to permanent housing",
                    "20% of people exiting our residential shelters will exit to stable housing"
                ]
                concatenated["Goal"] = [
                    "",
                    "",
                    "",
                    "35%",
                    "20%"
                ]

                # return the resultant pivot table
                return concatenated

            elif provider.lower() == "es":
                # Add the quarter and fiscal year columns
                leavers = QuarterAndFiscalYear(
                    data[
                        data["Entry Exit Provider Id"].isin(
                            self.departments[provider_type.lower()]
                        ) &
                        data["Entry Exit Exit Date"].notna()
                    ],
                    fill_na=False
                ).create_fy_q_columns()

                # Create an Exit Destination Column and fill it with values
                conds = [
                    leavers["Entry Exit Destination"].isin(self.perm_dest),
                    leavers["Entry Exit Destination"].isin(self.temp_dest),
                    (
                        ~(leavers["Entry Exit Destination"].isin(self.perm_dest)) &
                        ~(leavers["Entry Exit Destination"].isin(self.temp_dest))
                    )
                ]
                choices = ["Perm", "Stable", "Homeless"]
                leavers["Exit Destination"] = np.select(conds, choices, default="Homeless")

                # Create the pivot tables showing exit destination count by
                # quarter
                q_perm = pd.pivot_table(
                    leavers[
                        leavers["Exit Destination"] == "Perm"
                    ],
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_perm["FYTD"] = len(
                    leavers[
                        leavers["Exit Destination"] == "Perm"
                    ].index
                )

                q_stable = pd.pivot_table(
                    leavers[
                        leavers["Exit Destination"] == "Stable"
                    ],
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_stable["FYTD"] = len(
                    leavers[
                        leavers["Exit Destination"] == "Stable"
                    ].drop_duplicates(subset="Client Uid").index
                )

                q_any = pd.pivot_table(
                    leavers,
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_any["FYTD"] = len(
                    leavers.index
                )

                # add a % to destination rows
                percent_perm = (100*(q_perm / q_any)).round(2)
                percent_stab = (100*(q_stable / q_any)).round(2)

                # Concatenate the quarter based pivot tables into a single table
                concatenated = pd.concat(
                    [q_perm, q_stable, q_any, percent_perm, percent_stab],
                    ignore_index=True
                )


                # add metric and goal columns
                concatenated["Metric"] = [
                    "",
                    "",
                    "",
                    "15% of people exiting our emergency shelters will exit to permanent housing",
                    "10% of people exiting our emergency shelters will exit to stable housing"
                ]
                concatenated["Goal"] = [
                    "",
                    "",
                    "",
                    "15%",
                    "10%"
                ]

                # return the resultant pivot table
                return concatenated

            else:
                # Add the quarter and fiscal year columns
                leavers = QuarterAndFiscalYear(
                    data[
                        (
                            data["Entry Exit Provider Id"] == "Transition Projects (TPI) Housing - Clark Annex GPD - SP(4259)"
                        ) &
                        data["Entry Exit Exit Date"].notna()
                    ],
                    fill_na=False
                ).create_fy_q_columns()

                # Create an Exit Destination Column and fill it with values
                conds = [
                    leavers["Entry Exit Destination"].isin(self.perm_dest),
                    leavers["Entry Exit Destination"].isin(self.temp_dest),
                    (
                        ~(leavers["Entry Exit Destination"].isin(self.perm_dest)) &
                        ~(leavers["Entry Exit Destination"].isin(self.temp_dest))
                    )
                ]
                choices = ["Perm", "Stable", "Homeless"]
                leavers["Exit Destination"] = np.select(conds, choices, default="Homeless")

                # Create the pivot tables showing exit destination count by
                # quarter
                q_perm = pd.pivot_table(
                    leavers[
                        leavers["Exit Destination"] == "Perm"
                    ].drop_duplicates(subset=["Client Uid", "Entry Exit Exit Date Quarter"]),
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_perm["FYTD"] = len(
                    leavers[
                        leavers["Exit Destination"] == "Perm"
                    ].drop_duplicates(subset="Client Uid").index
                )

                q_any = pd.pivot_table(
                    leavers.drop_duplicates(subset=["Client Uid", "Entry Exit Exit Date Quarter"]),
                    columns="Entry Exit Exit Date Quarter",
                    values="Client Uid",
                    aggfunc=len
                )
                q_any["FYTD"] = len(
                    leavers.drop_duplicates(subset="Client Uid").index
                )

                # add a % to destination rows
                percent_perm = (100*(q_perm / q_any)).round(2)

                # Concatenate the quarter based pivot tables into a single table
                concatenated = pd.concat(
                    [q_perm, q_any, percent_perm],
                    ignore_index=True
                )


                # add metric and goal columns
                concatenated["Metric"] = [
                    "",
                    "",
                    "85% of Grant and Per Diem participants will exit to permanent housing"
                ]
                concatenated["Goal"] = [
                    "",
                    "",
                    "85%"
                ]

                # return the resultant pivot table
                return concatenated

        if dept.lower() == "agency":
            return combined(data, provider_type)
        elif dept.lower() == "housing":
            return detail(data, provider_type)
        elif dept.lower() == "ca bm":
            return combined(data, provider_type)
        elif dept.lower() == "cagpd":
            return detail(data, provider_type)
        else:
            pass


    def percent_placed_into_perm_poc(self, placements_df, services_df, dept):
        """
        metric: 41% of people placed into permanent housing will be people of
        color

        used by: Agency, Housing Case Management, Veterans Case Management

        :param placements_df:  a pandas pivot table generated from the
        placements v.4.0.xls Art Report

        :services_df:  a pandas pivot table generated from the All agency All
        Services.xls Art report

        :param dept: a string; either agency, housing, vets

        :return:
        """
        data = QuarterAndFiscalYear(
            placements_df,
            fill_na=False
        ).create_fy_q_columns().dropna(subset=["Intervention Type (TPI)(8745)"])
        poc = CreatePOCList(services_df).return_poc_list()

        if dept.lower() == "agency":
            # create a sub-datatable containing only participants who idenfity
            # as a person of color and were placed into permanent housing
            perm_poc = data[
                data["Client Uid"].isin(poc) &
                data["Intervention Type (TPI)(8745)"].str.contains("Permanent")
            ]

            # create a sub-datatable containing only participants who idenfity
            # as a person of color and were placed into permanent housing
            perm_all = data[
                data["Intervention Type (TPI)(8745)"].str.contains("Permanent")
            ]

            # create a pivot table showing poc placed into permanent housing by
            # year and quarter
            poc_q_pivot = pd.pivot_table(
                perm_poc.drop_duplicates(subset=[
                    "Client Uid",
                    "Placement Date(3072) Fiscal Year",
                    "Placement Date(3072) Fiscal Quarter"
                ]),
                index=["Placement Date(3072) Fiscal Year"],
                columns=["Placement Date(3072) Quarter"],
                values="Client Uid",
                aggfunc=len
            )


            # create a pivot table showing poc placed into permanent housing by
            # year
            poc_y_pivot = pd.pivot_table(
                perm_poc.drop_duplicates(subset=[
                    "Client Uid",
                    "Placement Date(3072) Fiscal Year"
                ]),
                index=["Placement Date(3072) Fiscal Year"],
                values="Client Uid",
                aggfunc=len
            )

            # create a pivot table showing all placed into permanent housing by
            # year and quarter
            all_q_pivot = pd.pivot_table(
                perm_all.drop_duplicates(subset=[
                    "Client Uid",
                    "Placement Date(3072) Fiscal Year",
                    "Placement Date(3072) Fiscal Quarter"
                ]),
                index=["Placement Date(3072) Fiscal Year"],
                columns=["Placement Date(3072) Quarter"],
                values="Client Uid",
                aggfunc=len
            )


            # create a pivot table showing all placed into permanent housing by
            # year
            all_y_pivot = pd.pivot_table(
                perm_all.drop_duplicates(subset=[
                    "Client Uid",
                    "Placement Date(3072) Fiscal Year"
                ]),
                index=["Placement Date(3072) Fiscal Year"],
                values="Client Uid",
                aggfunc=len
            )

            # merge each year and quarter pivot then concatenate the two into a
            # single pivot table
            merge_pivot_poc = poc_q_pivot.merge(
                poc_y_pivot,
                how="outer",
                left_index=True,
                right_index=True
            ).rename_axis(None)


            merge_pivot_all = all_q_pivot.merge(
                all_y_pivot,
                how="outer",
                left_index=True,
                right_index=True
            ).rename_axis(None)

            concat_pivot = pd.concat(
                [merge_pivot_poc, merge_pivot_all],
                ignore_index=True
            ).rename(
                columns={"Client Uid": "FYTD"}
            )

            # Add a % PoC row showing the # poc / # all then add the Dept and
            # Metric columns
            concat_pivot.loc["% PoC"] = (
                100*concat_pivot.loc[0]/concat_pivot.loc[1]
            ).round(2)
            concat_pivot["Metric"] = "41% of people placed into permanent housing will be people of color"
            concat_pivot["Goal"] = "41%"

            return concat_pivot

        elif dept.lower() == "vets":
            # create a sub-datatable containing only participants who idenfity
            # as a person of color and were placed into permanent housing
            perm_poc = data[
                data["Client Uid"].isin(poc) &
                data["Department Placed From(3076)"].str.contains("SSVF") &
                data["Intervention Type (TPI)(8745)"].str.contains("Permanent")
            ]

            # create a sub-datatable containing only participants who idenfity
            # as a person of color and were placed into permanent housing
            perm_all = data[
                data["Department Placed From(3076)"].str.contains("SSVF") &
                data["Intervention Type (TPI)(8745)"].str.contains("Permanent")
            ]

            # create a pivot table showing poc placed into permanent housing by
            # year and quarter
            poc_q_pivot = pd.pivot_table(
                perm_poc.drop_duplicates(subset=[
                    "Client Uid",
                    "Placement Date(3072) Fiscal Year",
                    "Placement Date(3072) Fiscal Quarter"
                ]),
                index=["Placement Date(3072) Fiscal Year"],
                columns=["Placement Date(3072) Quarter"],
                values="Client Uid",
                aggfunc=len
            )


            # create a pivot table showing poc placed into permanent housing by
            # year
            poc_y_pivot = pd.pivot_table(
                perm_poc.drop_duplicates(subset=[
                    "Client Uid",
                    "Placement Date(3072) Fiscal Year"
                ]),
                index=["Placement Date(3072) Fiscal Year"],
                values="Client Uid",
                aggfunc=len
            )

            # create a pivot table showing all placed into permanent housing by
            # year and quarter
            all_q_pivot = pd.pivot_table(
                perm_all.drop_duplicates(subset=[
                    "Client Uid",
                    "Placement Date(3072) Fiscal Year",
                    "Placement Date(3072) Fiscal Quarter"
                ]),
                index=["Placement Date(3072) Fiscal Year"],
                columns=["Placement Date(3072) Quarter"],
                values="Client Uid",
                aggfunc=len
            )


            # create a pivot table showing all placed into permanent housing by
            # year
            all_y_pivot = pd.pivot_table(
                perm_all.drop_duplicates(subset=[
                    "Client Uid",
                    "Placement Date(3072) Fiscal Year"
                ]),
                index=["Placement Date(3072) Fiscal Year"],
                values="Client Uid",
                aggfunc=len
            )

            # merge each year and quarter pivot then concatenate the two into a
            # single pivot table
            merge_pivot_poc = poc_q_pivot.merge(
                poc_y_pivot,
                how="outer",
                left_index=True,
                right_index=True
            ).rename_axis(None)


            merge_pivot_all = all_q_pivot.merge(
                all_y_pivot,
                how="outer",
                left_index=True,
                right_index=True
            ).rename_axis(None)

            concat_pivot = pd.concat(
                [merge_pivot_poc, merge_pivot_all],
                ignore_index=True
            ).rename(
                columns={"Client Uid": "FYTD"}
            )

            # Add a % PoC row showing the # poc / # all then add the Dept and
            # Metric columns
            concat_pivot.loc["% PoC"] = (
                100*(concat_pivot.loc[0]/concat_pivot.loc[1])
            ).round(2)
            concat_pivot["Metric"] = "41% of participants served will be people of color"
            concat_pivot["Goal"] = "41%"

            return concat_pivot

        elif dept.lower() == "housing":
            # create a sub-datatable containing only participants who idenfity
            # as a person of color and were placed into permanent housing
            perm_poc = data[
                data["Client Uid"].isin(poc) &
                (
                    (
                        data["Department Placed From(3076)"].str.contains("ACCE") &
                        ~(placements_df["Reporting Program (TPI)(8748)"] == "Ticket Home - Served")
                    ) |
                    data["Department Placed From(3076)"].str.contains("Residen")
                ) &
                data["Intervention Type (TPI)(8745)"].str.contains("Permanent")
            ]

            # create a sub-datatable containing only participants who idenfity
            # as a person of color and were placed into permanent housing
            perm_all = data[
                (
                    (
                        data["Department Placed From(3076)"].str.contains("ACCE") &
                        ~(placements_df["Reporting Program (TPI)(8748)"] == "Ticket Home - Served")
                    ) |
                    data["Department Placed From(3076)"].str.contains("Residen")
                ) &
                data["Intervention Type (TPI)(8745)"].str.contains("Permanent")
            ]

            # create a pivot table showing poc placed into permanent housing by
            # year and quarter
            poc_q_pivot = pd.pivot_table(
                perm_poc.drop_duplicates(subset=[
                    "Client Uid",
                    "Placement Date(3072) Fiscal Year",
                    "Placement Date(3072) Fiscal Quarter"
                ]),
                index=["Placement Date(3072) Fiscal Year"],
                columns=["Placement Date(3072) Quarter"],
                values="Client Uid",
                aggfunc=len
            )


            # create a pivot table showing poc placed into permanent housing by
            # year
            poc_y_pivot = pd.pivot_table(
                perm_poc.drop_duplicates(subset=[
                    "Client Uid",
                    "Placement Date(3072) Fiscal Year"
                ]),
                index=["Placement Date(3072) Fiscal Year"],
                values="Client Uid",
                aggfunc=len
            )

            # create a pivot table showing all placed into permanent housing by
            # year and quarter
            all_q_pivot = pd.pivot_table(
                perm_all.drop_duplicates(subset=[
                    "Client Uid",
                    "Placement Date(3072) Fiscal Year",
                    "Placement Date(3072) Fiscal Quarter"
                ]),
                index=["Placement Date(3072) Fiscal Year"],
                columns=["Placement Date(3072) Quarter"],
                values="Client Uid",
                aggfunc=len
            )


            # create a pivot table showing all placed into permanent housing by
            # year
            all_y_pivot = pd.pivot_table(
                perm_all.drop_duplicates(subset=[
                    "Client Uid",
                    "Placement Date(3072) Fiscal Year"
                ]),
                index=["Placement Date(3072) Fiscal Year"],
                values="Client Uid",
                aggfunc=len
            )

            # merge each year and quarter pivot then concatenate the two into a
            # single pivot table
            merge_pivot_poc = poc_q_pivot.merge(
                poc_y_pivot,
                how="outer",
                left_index=True,
                right_index=True
            ).rename_axis(None)


            merge_pivot_all = all_q_pivot.merge(
                all_y_pivot,
                how="outer",
                left_index=True,
                right_index=True
            ).rename_axis(None)

            concat_pivot = pd.concat(
                [merge_pivot_poc, merge_pivot_all],
                ignore_index=True
            ).rename(
                columns={"Client Uid": "FYTD"}
            )

            # Add a % PoC row showing the # poc / # all then add the Dept and
            # Metric columns
            concat_pivot.loc["% PoC"] = (
                100*(concat_pivot.loc[0]/concat_pivot.loc[1])
            ).round(2)
            concat_pivot["Metric"] = "41% of participants served will be people of color"
            concat_pivot["Goal"] = "41%"

            return concat_pivot


    def percent_referrals_successful(self, services_df, needs_df):
        """
        metric: 70% of referrals will result in a connection to care

        used by: Wellness Access

        :param services_df: a pandas data frame from the all services + needs
        status.xls ART report

        :param needs_df:a pandas data frame from the all services + needs
        status.xls ART report

        :return: a pandas dataframe
        """

        # create local version of the needs_df
        needs = needs_df[
            ["Client Uid", "Need Date Set", "Need Status", "Need Outcome"]
        ]

        # add quarter and fiscal year columns to a local copy of services_df
        services = QuarterAndFiscalYear(
            services_df[
                services_df["Service Provider Specific Code"].isin(self.wa_referrals) &
                services_df["Service Provide Provider"].isin(self.departments["well"])
            ],
            fill_na=False
        ).create_fy_q_columns()

        # merger the needs and services dataframes on client uid, service
        # provide start date, and need date set
        merged = services.merge(
            needs,
            how="left",
            left_on=["Client Uid", "Service Provide Start Date"],
            right_on=["Client Uid", "Need Date Set"]
        )

        # create a pivot table showing need satutus fully met referrals by
        # quarter do no de duplicate
        q_met = pd.pivot_table(
            merged[merged["Need Outcome"] == "Fully Met"],
            index="Service Provide Start Date Fiscal Year",
            columns="Service Provide Start Date Quarter",
            values="Client Uid",
            aggfunc=len
        )

        # add a fytd column with no deduplication
        q_met["FYTD"] = len(merged[merged["Need Outcome"] == "Fully Met"].index)

        # create a pivot table showing any need status by quarter
        q_served = pd.pivot_table(
            merged,
            index="Service Provide Start Date Fiscal Year",
            columns="Service Provide Start Date Quarter",
            values="Client Uid",
            aggfunc=len
        )

        # add a fytd column
        q_served["FYTD"] = len(merged.index)

        # create a % successfull dataframe
        percent = 100*(q_met / q_served).round(2)

        # concatenate the pivot tables and dataframes
        concatenated = pd.concat([q_met, q_served, percent], ignore_index=True)

        # add metric and goal columns
        concatenated["Metric"] = "70% of referrals will result in a connection to care"
        concatenated["Goal"] = "70%"

        # return the resulting dataframe
        return concatenated


    def percent_retaining_post_12_months(self, follow_ups_df):
        """
        metric: 70% of people housed will remain in hosing 12-months post
        subsidy

        used by: Agency, Veterans

        :param follow_ups_df: a data frame created from the follow-ups.xls Art
        report

        :return:
        """

        # Create a local copy of follow_ups_df
        fu = QuarterAndFiscalYear(
            follow_ups_df[
                follow_ups_df["End of Subsidy Date(2516)"].notna() &
                follow_ups_df["Actual Follow Up Date(2518)"].notna() &
                (follow_ups_df["End of Subsidy Date(2516)"] < follow_ups_df["Actual Follow Up Date(2518)"])
            ],
            fill_na=False
        ).create_fy_q_columns()

        # Add a new column showing the months between end of subsidy and
        # follow-up
        fu["End of Subsidy Date(2516)"] = pd.to_datetime(fu["End of Subsidy Date(2516)"]).dt.date
        fu["Actual Follow Up Date(2518)"] = pd.to_datetime(fu["Actual Follow Up Date(2518)"]).dt.date
        fu["Months Post Subsidy"] = (
            fu["Actual Follow Up Date(2518)"]- fu["End of Subsidy Date(2516)"]
        ) / np.timedelta64(1,"M")

        # create a pivot table showing all who retained housing between 11 and
        # 13 months post subsidy
        pos_pivot = pd.pivot_table(
            fu[
                (fu["Months Post Subsidy"] > 10) &
                (fu["Months Post Subsidy"] < 14) &
                (fu["Is Client Still in Housing?(2519)"] == "Yes (HUD)")
            ].sort_values(by="Months Post Subsidy", ascending=False).drop_duplicates(subset=["Client Uid", "Actual Follow Up Date(2518) Fiscal Year", "Actual Follow Up Date(2518) Quarter"]),
            index="Actual Follow Up Date(2518) Fiscal Year",
            columns="Actual Follow Up Date(2518) Quarter",
            values="Client Uid",
            aggfunc=len
        ).rename_axis(None)

        # Create annualized column in the above pivot table
        pos_pivot["FYTD"] = len(
            fu[
                (fu["Months Post Subsidy"] > 10) &
                (fu["Months Post Subsidy"] < 14) &
                (fu["Is Client Still in Housing?(2519)"] == "Yes (HUD)")
            ].sort_values(by="Months Post Subsidy", ascending=False).drop_duplicates(subset="Client Uid").index
        )


        # create a data table with any 12-month post subsidy follow-up allowing
        # a follow-up to be made anywhere between 11 and 13 months post subsidy.
        all_pivot = pd.pivot_table(
            fu[
                (fu["Months Post Subsidy"] > 10) &
                (fu["Months Post Subsidy"] < 13)
            ].sort_values(by="Months Post Subsidy", ascending=False).drop_duplicates(subset=["Client Uid", "Actual Follow Up Date(2518) Fiscal Year", "Actual Follow Up Date(2518) Quarter"]),
            index="Actual Follow Up Date(2518) Fiscal Year",
            columns="Actual Follow Up Date(2518) Quarter",
            values="Client Uid",
            aggfunc=len
        )

        # Create annualized column in the above pivot table
        all_pivot["FYTD"] = len(
            fu[
                (fu["Months Post Subsidy"] > 10) &
                (fu["Months Post Subsidy"] < 13)
            ].sort_values(by="Months Post Subsidy", ascending=False).drop_duplicates(subset="Client Uid").index
        )

        # Add a % row dividing the previous colomns and multiplying the result
        # by 100


        # Merge the pivot tables
        final_pivot = pd.concat(
            [pos_pivot, all_pivot],
            ignore_index=True
        )

        # Add question and goal columns
        final_pivot.loc["% of participants retaining housing"] = (
            100*(final_pivot.loc[0]/final_pivot.loc[1])
        ).round(2)
        final_pivot["Metric"] = "70% of participants will retain housing 12 months post subsidy"
        final_pivot["Goal"] = "70%"

        # return the results
        return final_pivot


    def percent_served_poc(self, services_df, dept):
        """
        metric: 41% of participants served will be people of color

        used by: resource center, outreach/CHAT,
        health

        :param services_df: a pandas dataframe created from the all services
        (all tpi).xls report created by ART

        :param dept: a string for a shortened department name for example
        retention cm would use ret. see the self.departments dict for a full
        listing.

        :return: a pivot table
        """
        # add quarter and fiscal year columns to a local copy of the data frame
        data = QuarterAndFiscalYear(services_df[
            services_df["Service Provide Provider"].isin(self.departments[dept])
        ].drop_duplicates(subset="Client Uid"), fill_na=False).create_fy_q_columns()

        # create a list of all poc
        poc = CreatePOCList(services_df).return_poc_list()

        # create a pivot table showing poc data
        poc_pivot = pd.pivot_table(
            data[
                data["Client Uid"].isin(poc)
            ].drop_duplicates(subset=["Client Uid", "Service Provide Start Date Quarter"]),
            index="Service Provide Start Date Fiscal Year",
            columns="Service Provide Start Date Quarter",
            values="Client Uid",
            aggfunc=len
        )

        # add a fytd column to the poc pivot table
        poc_pivot["FYTD"] = len(data[data["Client Uid"].isin(poc)].index)

        # create a non_poc pivot table
        all_pivot = pd.pivot_table(
            data.drop_duplicates(subset=["Client Uid", "Service Provide Start Date Quarter"]),
            index="Service Provide Start Date Fiscal Year",
            columns="Service Provide Start Date Quarter",
            values="Client Uid",
            aggfunc=len
        )

        # add a fytd column to the poc pivot table
        all_pivot["FYTD"] = len(data.index)


        # create new pivot table showing % of all who are poc
        percent_pivot = (100*(poc_pivot / all_pivot)).round(2)

        # concatenate the two pivot tables
        concatenated = pd.concat(
            [poc_pivot, all_pivot, percent_pivot],
            ignore_index=True
        )

        # add metrics and goals columns
        concatenated["Metric"] = "41% of participants served will be people of color"
        concatenated["Goal"] = "41%"
        concatenated.index = ["PoC", "All", "% PoC"]

        # return the concatenated data frame of pivot tables
        return concatenated


    def percent_w_hf_ss(self, services_df, dept):
        pass


    def percent_w_ss_service(self, entries_df, services_df, quarter_end, fiscal_year, dept):
        """
        metric: 50% of participants enrolled in our retention program will
        engage in supportive services; 75% of guests will connect to a supportive
        service; 75% of guests will connect to a supportive service

        used by: Retention CM, Residential Shelter, Emergency Shelter

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
                entries_df["Entry Exit Provider Id"].isin(self.departments[dept])
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

        # create a pivot table for all participants with an open entry during a
        # given quarter
        all_pivot_dict = {
            "Q1": [q_check["Q1"].sum()],
            "Q2": [q_check["Q2"].sum()],
            "Q3": [q_check["Q3"].sum()],
            "Q4": [q_check["Q4"].sum()]
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


    def percent_w_vi_spdat(self, entries_df, spdat_df, dept, quarter_end):
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
                entries_df["Entry Exit Provider Id"].isin(self.departments[dept])
            ],
            "specify",
            quarter_end,
            True
        ).create_fy_q_columns()

        # use the return_quarters function to create a dataframe of participants
        # with an entry and a vi-spdat by quarter
        q_spdated = return_quarters(
            entries[entries["Client Uid"].isin(spdat["Client Uid"])]
        ).drop_duplicates(subset="Client Uid")

        # create a pivot table from the q_spdated dataframe
        all_spdated_dict = {
            "Q1": [q_spdated["Q1"].sum()],
            "Q2": [q_spdated["Q2"].sum()],
            "Q3": [q_spdated["Q3"].sum()],
            "Q4": [q_spdated["Q4"].sum()]
        }
        all_spdated = pd.DataFrame.from_dict(all_spdated_dict)
        all_spdated["FYTD"] = len(entries[entries["Client Uid"].isin(spdat)].drop_duplicates(subset="Client Uid").index)

        # use the return_quarters function to create a dataframe of all participants
        # with a provider entry
        q_all = return_quarters(entries).drop_duplicates(subset="Client Uid")

        # create a pivot table from the q_all dataframe
        all_dict = {
            "Q1": [q_all["Q1"].sum()],
            "Q2": [q_all["Q2"].sum()],
            "Q3": [q_all["Q3"].sum()],
            "Q4": [q_all["Q4"].sum()]
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


if __name__ == "__main__":
    a = AllFunctions()
    print(a.percent_day_hf_ss(pd.read_excel(askopenfilename(title="services")),[datetime(year=2018, month=10, day=1)]))
