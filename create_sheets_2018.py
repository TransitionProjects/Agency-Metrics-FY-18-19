"""
A revision of the create sheets script for the 2018-2019 fiscal year and its
updated reporting requirements.
"""

__author__ = "David Marienburg"
__maintainer__ = "David Marienburg"
__version__ = "2.0"

import pandas as pd
from all_functions import AllFunctions as af

class Department:
    """
    This sets up the base department class that all other departmetns will be
    modeled upon.  Each class will create its own unique process method to
    reflect its unique reporting requirements.  This class will call the
    return_output method after completing the creation of the self.output list
    of tuples.

    :param services_file: a file path from askopenfilename
    :param entries_file: a file path from askopenfilename
    :param placements_file: a file path from askopenfilename
    :param followups_file: a file path from askopenfilename
    """
    def __init__(
        self,
        services_file,
        entries_file
    ):
        self.original_services = pd.read_excel(services_file, sheet_name="Service Data")
        self.original_needs = pd.read_excel(services_file, sheet_name="Need Data")
        self.original_entries = pd.read_excel(entries_file, sheet_name="Report 1")
        self.output = []

    def print_all(self):
        print(pd.DataFrame(self.output, columns=["Question", "Goal", "Metric"]))


class Agency(Department):
    def __init__(
        self,
        services_file,
        entries_file,
        placements_file,
        followups_file_a
    ):
        super(Agency, self).__init__(
            services_file,
            entries_file
        )
        self.original_followups_a = pd.read_excel(followups_file_a, sheet_name="Report 1")
        self.original_placements = pd.read_excel(placements_file, sheet_name="Placement Data")

    def process(self):
        self.output = [
            af().count_placed_into_perm(self.original_placements, "agency"),
            af().percent_placed_into_perm_poc(self.original_placements, self.original_services, "agency"),
            af().percent_retaining_post_12_months(self.original_followups_a),
            af().percent_exits_by_destination(self.original_entries, "res", "agency"),
            af().percent_exits_by_destination(self.original_entries, "es", "agency")
        ]

        return pd.concat(self.output, ignore_index=True)


class Retention(Department):
    def __init__(
        self,
        services_file,
        entries_file,
        placements_file,
        followups_file_r,
        quarter_end,
        fiscal_year
    ):
        super(Retention, self).__init__(
            services_file,
            entries_file
        )
        self.original_placements = pd.read_excel(placements_file, sheet_name="Placement Data")
        self.original_followups_r = pd.read_excel(followups_file_r, sheet_name="Report 1")
        self.quarter_end = quarter_end
        self.fiscal_year = fiscal_year

    def process(self):
        self.output = [
            af().percent_retaining_post_12_months(self.original_followups_r),
            af().percent_w_ss_service(self.original_entries, self.original_services, self.quarter_end, self.fiscal_year, "retention")
        ]
        return pd.concat(self.output, ignore_index=True)


class HousingCM(Department):
    def __init__(
        self,
        services_file,
        entries_file,
        placements_file
    ):
        super(HousingCM, self).__init__(
            services_file,
            entries_file
        )
        self.original_placements = pd.read_excel(placements_file, sheet_name="Placement Data")

    def process(self):
        self.output = [
            af().count_placed_into_perm(self.original_placements, "housing"),
            af().percent_exits_by_destination(self.original_entries, "res", "housing"),
            af().percent_exits_by_destination(self.original_entries, "es", "housing"),
            af().percent_placed_into_perm_poc(self.original_placements, self.original_services, "housing")
        ]

        return pd.concat(self.output, ignore_index=True)


class Veterans(Department):
    def __init__(
        self,
        services_file,
        entries_file,
        placements_file,
        followups_file_v
    ):
        super(Veterans, self).__init__(
            services_file,
            entries_file
        )
        self.original_placements = pd.read_excel(placements_file, sheet_name="Placement Data")
        self.original_followups_v = pd.read_excel(followups_file_v, sheet_name="Report 1")

    def process(self):
        self.output = [
            af().count_placed_into_perm(self.original_placements, "vets"),
            af().count_placed_into_ep(self.original_placements),
            af().percent_retaining_post_12_months(self.original_followups_v),
            af().percent_placed_into_perm_poc(self.original_placements, self.original_services, "vets")
        ]

        return pd.concat(self.output, ignore_index=True)


class Resource(Department):
    def __init__(
        self,
        services_file,
        entries_file
    ):
        super(Resource, self).__init__(
            services_file,
            entries_file
        )

    def process(self):
        self.output = [
            af().count_served_by_provider(self.original_services, "rec"),
            af().count_served_with_hygiene_services(self.original_services, "rec"),
            af().percent_served_poc(self.original_services, "rec"),
            # af().percent_w_hf_ss(self.original_services, "rec")
        ]

        return pd.concat(self.output, ignore_index=True)


class Permanent(Department):
    def __init__(
        self,
        services_file,
        entries_file
    ):
        super(Permanent, self).__init__(
            services_file,
            entries_file
        )

    def process(self):
        self.output = [
            af().percent_exits_by_destination(self.original_entries, "perm", "cagpd"),
            af().percent_exits_by_destination(self.original_entries, "perm", "ca bm")
        ]

        return pd.concat(self.output, ignore_index=True)


class Residential(Department):
    def __init__(
        self,
        services_file,
        entries_file,
        spdat_file,
        quarter_end,
        fiscal_year
    ):
        super(Residential, self).__init__(
            services_file,
            entries_file
        )
        self.quarter_end = quarter_end
        self.fiscal_year = fiscal_year
        self.original_spdat = pd.read_excel(spdat_file, sheet_name="Report 1")

    def process(self):
        self.output = [
            af().count_entered_into_provider(self.original_entries, "res", self.quarter_end, self.fiscal_year),
            af().percent_w_ss_service(self.original_entries, self.original_services, self.quarter_end, self.fiscal_year, "res"),
            af().percent_w_vi_spdat(self.original_entries, self.original_spdat, "res", self.quarter_end),
            af().percent_entries_poc(self.original_entries, "res", self.quarter_end)
        ]

        return pd.concat(self.output, ignore_index=True)


class Emergency(Department):
    def __init__(
        self,
        services_file,
        entries_file,
        exclusions_file,
        spdat_file,
        quarter_end,
        fiscal_year

    ):
        super(Emergency, self).__init__(
            services_file,
            entries_file
        )
        self.original_spdat = pd.read_excel(spdat_file, sheet_name="Report 1")
        self.original_exclusions = pd.read_excel(exclusions_file, sheet_name="Exclusions")
        self.quarter_end = quarter_end
        self.fiscal_year = fiscal_year


    def process(self):
        self.output = [
            af().count_entered_into_provider(self.original_entries, "es", self.quarter_end, self.fiscal_year),
            af().count_exclusions_by_provider(self.original_exclusions, "es", self.quarter_end),
            af().percent_entries_poc(self.original_entries, "es", self.quarter_end),
            af().percent_w_ss_service(self.original_entries, self.original_services, self.quarter_end, self.fiscal_year, "es"),
            af().percent_w_vi_spdat(self.original_entries, self.original_spdat, "es", self.quarter_end)
        ]

        return pd.concat(self.output, ignore_index=True)


class RentWell(Department):
    def __init__(
        self,
        services_file,
        entries_file

    ):
        super(RentWell, self).__init__(
            services_file,
            entries_file
        )

    def process(self):
        self.output = [
            af().count_attend_rent_well(self.original_services)
        ]

        return pd.concat(self.output, ignore_index=True)


class Outreach(Department):
    def __init__(
        self,
        services_file,
        entries_file,
        vi_spdat_file,
        quarter_end,
        fiscal_year

    ):
        super(Outreach, self).__init__(
            services_file,
            entries_file
        )
        self.original_spdat = pd.read_excel(vi_spdat_file, sheet_name="Report 1")
        self.quarter_end = quarter_end
        self.fiscal_year = fiscal_year

    def process(self):
        self.output = [
            af().count_spdated(self.original_spdat),
            af().count_document_ready(self.original_spdat),
            af().count_entered_into_provider(self.original_entries, "TicketHome", self.quarter_end, self.fiscal_year),
            af().percent_served_poc(self.original_services, "out")
        ]

        return pd.concat(self.output, ignore_index=True)


class Health(Department):
    def __init__(
        self,
        services_file,
        entries_file

    ):
        super(Health, self).__init__(
            services_file,
            entries_file
        )

    def process(self):
        self.output = [
            af().count_referred_to_h_w_service(self.original_services),
            af().percent_referrals_successful(self.original_services, self.original_needs),
            af().percent_served_poc(self.original_services, "well")
        ]

        return pd.concat(self.output, ignore_index=True)

if __name__ == "__main__":
    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import asksaveasfilename
    from datetime import datetime

    # create file location objects for all relevant reports
    services_file = askopenfilename(title="Services")
    entries_file = askopenfilename(title="Entries")
    placements_file = askopenfilename(title="Placements")
    follow_ups_a_file = askopenfilename(title="Follow Ups Agency")
    follow_ups_r_file = askopenfilename(title="Follow Ups Retention")
    follow_ups_v_file = askopenfilename(title="Follow Ups Vets")
    spdat_file = askopenfilename(title="VI-SPDAT")
    exclusions_file = askopenfilename(title="Exclusions")

    # create class objects for each departments metrics
    agency = Agency(
        services_file,
        entries_file,
        placements_file,
        follow_ups_a_file
    ).process()
    retention = Retention(
        services_file,
        entries_file,
        placements_file,
        follow_ups_r_file,
        datetime(year=2018, month=9, day=30),
        "FY 18-19"
    ).process()
    housingcm = HousingCM(
        services_file,
        entries_file,
        placements_file
    ).process()
    vets = Veterans(
        services_file,
        entries_file,
        placements_file,
        follow_ups_v_file
    ).process()
    resource = Resource(
        services_file,
        entries_file
    ).process()
    perm = Permanent(
        services_file,
        entries_file
    ).process()
    res = Residential(
        services_file,
        entries_file,
        spdat_file,
        datetime(year=2018, month=9, day=30),
        "FY 18-19"
    ).process()
    es = Emergency(
        services_file,
        entries_file,
        exclusions_file,
        spdat_file,
        datetime(year=2018, month=9, day=30),
        "FY 18-19"
    ).process()
    rent = RentWell(
        services_file,
        entries_file
    ).process()
    out = Outreach(
        services_file,
        entries_file,
        spdat_file,
        datetime(year=2018, month=9, day=30),
        "FY 18-19"
    ).process()
    health = Health(
        services_file,
        entries_file
    ).process()

    # establish writer object and save the output to a spreadsheet
    writer = pd.ExcelWriter(asksaveasfilename(), engine="xlsxwriter")
    agency.to_excel(writer, sheet_name="Agency", index=False)
    housingcm.to_excel(writer, sheet_name="Housing CM", index=False)
    retention.to_excel(writer, sheet_name="Retention", index=False)
    housingcm.to_excel(writer, sheet_name="Housing CM", index=False)
    vets.to_excel(writer, sheet_name="Vets", index=False)
    resource.to_excel(writer, sheet_name="Resource Center", index=False)
    perm.to_excel(writer, sheet_name="CC and BM", index=False)
    res.to_excel(writer, sheet_name="Res Shelters", index=False)
    es.to_excel(writer, sheet_name="ES Shelters", index=False)
    rent.to_excel(writer, sheet_name="RentWell", index=False)
    out.to_excel(writer, sheet_name="Outreach", index=False)
    health.to_excel(writer, sheet_name="Healt and Wellness", index=False)
    writer.save()
