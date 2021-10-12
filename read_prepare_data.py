# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 10:12:26 2021

@author: Florian Jehn
"""
import os
import pandas as pd
import numpy as np

def read_ipcc_counts():
    """reads all counts for all reports and makes on df"""
    files = os.listdir(os.getcwd()+os.sep+"Results")
    all_df = pd.DataFrame()
    for file in files:
        file_df = pd.read_csv("Results" + os.sep + file, sep=";", index_col=0)
        file_df.columns = [file[:-4]]
        all_df = pd.concat([all_df, file_df], axis=1)
        
    return all_df.transpose()
        

def scale_counts(ipcc_counts):
    """scale the counts by overall sum"""
    sums = ipcc_counts.sum(axis=1)
    for col in ipcc_counts:
        ipcc_counts[col] = ipcc_counts[col]/sums*100
    return ipcc_counts
    
    
def read_meta():
    """reads in the meta data of the reports"""
    meta = pd.read_csv("Reports" + os.sep + "meta_data_reports.tsv", sep="\t")
    meta["Year"]  = meta["Year"].astype("str")
    return meta


def group_temps(ipcc_counts):
    ipcc_counts["0.5°C-2°C"] = ipcc_counts[" 0.5°C"] + ipcc_counts[" 1°C"] + ipcc_counts[" 1.5°C"] +ipcc_counts[" 2°C"] 
    ipcc_counts["2.5°C-4°C"] = ipcc_counts[" 2.5°C"] + ipcc_counts[" 3°C"] + ipcc_counts[" 3.5°C"] +ipcc_counts[" 4°C"] 
    ipcc_counts["≥4.5°C"] = ipcc_counts[" 4.5°C"] + ipcc_counts[" 5°C"] + ipcc_counts[" 5.5°C"] +ipcc_counts[" 6°C"] +ipcc_counts[" 6.5°C"] + ipcc_counts[" 7°C"] + ipcc_counts[" 7.5°C"] +ipcc_counts[" 8°C"] + ipcc_counts[" 8.5°C"] + ipcc_counts[" 9°C"] + ipcc_counts[" 9.5°C"] +ipcc_counts[" 10°C"] 
    return ipcc_counts.iloc[:,20:]
    

def merge_counts_meta(ipcc_counts, meta):
    return pd.merge(meta, ipcc_counts, right_index=True, left_on="count_names") 


def lookup_names():
    """"Returns lookup dict for different files names to merge them"""
    lookup_dict = {
        "IPCC_AR6_WGI_Full_Report":"counts_ReportsIPCCAR6WGIFullReportpdf_parsed",
        "SROCC_FullReport_FINAL":"counts_ReportsSROCCFullReportFINALpdf_parsed",
        "210714-IPCCJ7230-SRCCL-Complete-BOOK-HRES":"counts_Reports210714IPCCJ7230SRCCLCompleteBOOKHRESpdf_parsed",
        "SR15_Full_Report_Low_Res":"counts_ReportsSR15FullReportLowRespdf_parsed",
        "SYR_AR5_FINAL_full":"counts_ReportsSYRAR5FINALfullwcoverpdf_parsed",
        "ipcc_wg3_ar5_full":"counts_Reportsipccwg3ar5fullpdf_parsed",
        "WGIIAR5-PartA_FINAL":"counts_ReportsWGIIAR5PartBFINALpdf_parsed",
        "WGIIAR5-PartB_FINAL":"counts_ReportsWGIIAR5PartAFINALpdf_parsed",
        "WG1AR5_all_final":"counts_ReportsWG1AR5allfinalpdf_parsed",
        "SREX_Full_Report-1":"counts_ReportsSREXFullReport1pdf_parsed",
        "SRREN_Full_Report-1":"counts_ReportsSRRENFullReport1pdf_parsed",
        "ar4_syr_full_report":"counts_Reportsar4syrfullreportpdf_parsed",
        "ar4_wg2_full_report":"counts_Reportsar4wg2fullreportpdf_parsed",
        "ar4_wg1_full_report-1":"counts_Reportsar4wg1fullreport1pdf_parsed",
        "ar4_wg3_full_report-1":"counts_Reportsar4wg3fullreport1pdf_parsed",
        "sroc_full-1":"counts_Reportssrocfull1pdf_parsed",
        "srccs_wholereport-1":"counts_Reportssrccswholereport1pdf_parsed",
        "SYR_TAR_full_report":"counts_ReportsSYRTARfullreportpdf_parsed",
        "WGII_TAR_full_report-2":"counts_ReportsWGIITARfullreport2pdf_parsed",
        "WGI_TAR_full_report":"counts_ReportsWGITARfullreportpdf_parsed",
        "WGIII_TAR_full_report":"counts_ReportsWGIIITARfullreportpdf_parsed",
        "srl-en-1":"counts_Reportssrlen1pdf_parsed",
        "srtt-en-1":"counts_Reportssrtten1pdf_parsed",
        "emissions_scenarios-1":"counts_Reportsemissionsscenarios1pdf_parsed",
        "av-en-1":"counts_Reportsaven1pdf_parsed",
        "The-Regional-Impact":"counts_ReportsTheRegionalImpactpdf_parsed",
        "2nd-assessment-en-1":"counts_Reports2ndassessmenten1pdf_parsed",
        "ipcc_sar_wg_III_full_report":"counts_ReportsipccsarwgIIIfullreportpdf_parsed",
        "ipcc_sar_wg_II_full_report":"counts_ReportsipccsarwgIIfullreportpdf_parsed",
        "ipcc_sar_wg_I_full_report":"counts_ReportsipccsarwgIfullreportpdf_parsed",
        "climate_change_1994-2":"counts_Reportsclimatechange19942pdf_parsed",
        "ipcc-technical-guidelines-1994n-1":"counts_Reportsipcctechnicalguidelines1994n1pdf_parsed",
        "ipcc_wg_I_1992_suppl_report_full_report":"counts_ReportsipccwgI1992supplreportfullreportpdf_parsed",
        "ipcc_wg_II_1992_suppl_report_full_report":"counts_ReportsipccwgII1992supplreportfullreportpdf_parsed",
        "ipcc_90_92_assessments_far_full_report":"counts_Reportsipcc9092assessmentsfarfullreportpdf_parsed",
        "ipcc_far_wg_III_full_report":"counts_ReportsipccfarwgIIIfullreportpdf_parsed",
        "ipcc_far_wg_II_full_report":"counts_ReportsipccfarwgIIfullreportpdf_parsed",
        "ipcc_far_wg_I_full_report":"counts_ReportsipccfarwgIfullreportpdf_parsed",
        }
    return lookup_dict


def create_temp_keys():
    temps = []
    for i,temp in enumerate(np.arange(0.5,10.1,0.5)):
        if i % 2 != 0:
             temps.append(" "+str(int(temp))+"°C")
        else: 
             temps.append(" "+str(temp)+"°C" )
    return temps


def combine_all_raw_strings():
    """combines all raw strings into one big file to search through"""
    df = pd.DataFrame()
    reports = [file for file in os.listdir(os.getcwd() + os.sep + "Raw IPCC Strings") if file[-4:] == ".csv" ]
    for report in reports:
        print("Starting with " + report) 
        report_df = pd.read_csv(os.getcwd() + os.sep + "Raw IPCC Strings" + os.sep + report)
        df = pd.concat([df, report_df])
    df.to_csv("Raw IPCC Strings" + os.sep + "all_reports.csv")    
    
    

if __name__ == "__main__":
    combine_all_raw_strings()
