#!/usr/bin/env python
# -*- coding utf-8 -*-

import os
from annex import mkdir_p
from collections import OrderedDict

TESTMODE = False  #can swith off randomisation in all modules for debug purposese
BINS = 20  #number of bins for histograms

REPORT_ROUNDING = 2  #rounding of decimals for xls report
REPORT_PATH = '~/data/mirr_reports'     #relevent path to storing reports
report_directory = os.path.expanduser(os.path.normpath(REPORT_PATH))  #folder for saving xls reposts
mkdir_p(report_directory)  #creating this folder (only 1-time)

IS = OrderedDict()  #INCOME STATEMENT , format dic[field_name]=attr_name or blank
IS["Dates"] = ""
IS["Revenue"] = "revenue"
IS["Revenues electricity sales"] = "revenue_electricity"
IS["Revenues subsidy"] = "revenue_subsidy"
IS["Costs"] = "cost"
IS["Operational costs"] = "operational_cost"
IS["Development costs"] = "development_cost"
IS["EBITDA"] = "ebitda"
IS["Depreciation"] = "depreciation"
IS["EBIT"] = "ebit"
IS["Interest paid"] = "iterest_paid"
IS["EBT"] = "ebt"
IS["Taxes"] = "tax"
IS["Net earnings"] = "net_earning"

BS = OrderedDict()  #BALANCE SHEET , format dic[field_name]=attr_name or blank
BS["Dates"] = ""
BS["Fixed Assests"] = "fixed_asset"
BS["Current Assets"] = "current_asset"
#BS["Inventories"] = "inventory"
BS["Operating Receivables"] = "operating_receivable"
#BS["Short-Term Investments"] = "short_term_investment"
BS["Assets On Bank Accounts"] = "asset_bank_account"
BS["Assets"] = "asset"
BS["Equity"] = "equity"

BS["Paid-In Capital"] = "paid_in_capital"
BS["Retained Earnings"] = "retained_earning"
BS["Unallocated Earnings"] = "unallocated_earning"
BS["Financial And Operating Obligations"] = "financial_operating_obligation"
BS["Long-Term Loans"] = "long_term_loan"
#BS["Long-Term Operating Liabilities"] = "long_term_operating_liability"
BS["Short-Term Loans"] = "short_term_loan"
BS["Short-Term Debt to Suppliers"] = "short_term_debt_suppliers"
BS["Liabilities"] = "liability"
BS["Control"] = "control"

PROJECT_START = "Project Start"

CF = OrderedDict()  #CASH FLOW , format dic[field_name]=attr_name or blank
CF["Dates"] = ""
CF["FCF project"] = "fcf_project"
CF["FCF owners"] = "fcf_owners"

NPV = OrderedDict()  #NPV , format dic[field_name]=attr_name or blank
NPV["Dates"] = ""
NPV["NPV project"] = "pv_project"
NPV["NPV owners"] = "pv_owners"

IRR_REPORT_FIELD = 'irr_project_y'  #Name of IRR values
IRR_REPORT_FIELD2 = 'irr_owners_y'  #for statistics after simulation
NPV_REPORT_FIELD = 'npv_project_y'

REPORT_DEFAULT_NUMBER_ITERATIONS = 20

CORRELLATION_FIELDS = OrderedDict() # IRR ONE SHOULD HAVE NAME =IRR and be FIRST ONE
CORRELLATION_FIELDS["permit_procurement_duration"] = "main_configs.real_permit_procurement_duration"
CORRELLATION_FIELDS["construction_duration"] = "main_configs.real_construction_duration"
CORRELLATION_FIELDS["kWhFIT"] = "sm_configs.kWhFIT"
CORRELLATION_FIELDS["subsidy_delay"] = "sm_configs.subsidy_delay"
CORRELLATION_FIELDS["subsidy_duration"] = "sm_configs.subsidy_duration"

CORRELLATION_FIELDS["admin_costs"] = "ecm_configs.administrativeCosts"
CORRELLATION_FIELDS["admin_costs_growth_rate"] = "ecm_configs.administrativeCostsGrowth_rate"
CORRELLATION_FIELDS["ins_fee_equip"] = "ecm_configs.insuranceFeeEquipment"
CORRELLATION_FIELDS["dev_costs_perm_proc"] = "ecm_configs.developmentCostDuringPermitProcurement"
CORRELLATION_FIELDS["dev_costs_construct"] = "ecm_configs.developmentCostDuringConstruction"
CORRELLATION_FIELDS["interest_rate"] = "ecm_configs.debt_rate"
CORRELLATION_FIELDS["interest_rate_short"] = "ecm_configs.debt_rate_short"

CORRELLATION_FIELDS["average_degradation_rate"] = "average_degradation_rate"

CORRELLATION_IRR_FIELD = {"IRR": IRR_REPORT_FIELD}
CORRELLATION_NPV_FIELD = {"NPV": NPV_REPORT_FIELD}

ELPROD = OrderedDict()  #BLOCK in EXCEL with data about electricity production
ELPROD["Dates"] = ""
ELPROD["Solar insolation"] = "sun_insolation"
ELPROD["Production of electricity"] = "electricity_production"
ELPROD["Electricity prices"] = "electricity_prices"

SOURCE = OrderedDict()  #DATA FOR SECOND SHEET EXCEL
SOURCE["Main config"] = 'main_configs'
SOURCE["Economic config"] = 'ecm_configs'
SOURCE["Technology config"] = 'tm_configs'
SOURCE["subsidy config"] = 'sm_configs'
SOURCE["Energy config"] = 'em_configs'
