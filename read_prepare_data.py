# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 10:12:26 2021

@author: Florian Jehn
"""
import os
import pandas as pd
import numpy as np


def read_ipcc_counts_temp():
    """reads all counts of temperatures for all reports and makes on df"""
    files = os.listdir(os.getcwd()+os.sep+"Results"+ os.sep + "temperatures")
    all_df = pd.DataFrame()
    for file in files:
        file_df = pd.read_csv("Results" + os.sep + "temperatures" + os.sep + file, sep=";", index_col=0)
        file_df.columns = [file[:-4]]
        all_df = pd.concat([all_df, file_df], axis=1)
    return all_df.transpose()


def read_ipcc_counts_rfc():
    """reads all counts of reasons of concern for all reports and makes on df"""
    files = os.listdir(os.getcwd()+os.sep+"Results"+ os.sep + "reasons_for_concern")
    all_df = pd.DataFrame()
    for file in files:
        file_df = pd.read_csv("Results" + os.sep + "reasons_for_concern" + os.sep + file, sep=";", index_col=0)
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
    """groups the temperatures into three categories"""
    ipcc_counts["0.5°C-2°C"] = ipcc_counts[" 0.5°C"] + ipcc_counts[" 1°C"] + ipcc_counts[" 1.5°C"] +ipcc_counts[" 2°C"] 
    ipcc_counts["2.5°C-4°C"] = ipcc_counts[" 2.5°C"] + ipcc_counts[" 3°C"] + ipcc_counts[" 3.5°C"] +ipcc_counts[" 4°C"] 
    ipcc_counts["≥4.5°C"] = ipcc_counts[" 4.5°C"] + ipcc_counts[" 5°C"] + ipcc_counts[" 5.5°C"] +ipcc_counts[" 6°C"] +ipcc_counts[" 6.5°C"] + ipcc_counts[" 7°C"] + ipcc_counts[" 7.5°C"] +ipcc_counts[" 8°C"] + ipcc_counts[" 8.5°C"] + ipcc_counts[" 9°C"] + ipcc_counts[" 9.5°C"] +ipcc_counts[" 10°C"] 
    return ipcc_counts.iloc[:,20:]
    

def merge_counts_meta(ipcc_counts, meta):
    """merges the df with the counted temperatures/rfcs with the metadata"""
    return pd.merge(meta, ipcc_counts, right_index=True, left_on="count_names") 


def lookup_names():
    """"Returns lookup dict for different files names to merge them"""
    lookup_dict = {
        "IPCC_AR6_WGI_Full_Report":"counts_IPCC_AR6_WGI_Full_Report_parsed",
        "SROCC_FullReport_FINAL":"counts_SROCC_FullReport_FINAL_parsed",
        "210714-IPCCJ7230-SRCCL-Complete-BOOK-HRES":"counts_210714-IPCCJ7230-SRCCL-Complete-BOOK-HRES_parsed",
        "SR15_Full_Report_Low_Res":"counts_SR15_Full_Report_Low_Res_parsed",
        "SYR_AR5_FINAL_full":"counts_SYR_AR5_FINAL_full_wcover_parsed",
        "ipcc_wg3_ar5_full":"counts_ipcc_wg3_ar5_full_parsed",
        "WGIIAR5-PartA_FINAL":"counts_WGIIAR5-PartA_FINAL_parsed",
        "WGIIAR5-PartB_FINAL":"counts_WGIIAR5-PartB_FINAL_parsed",
        "WG1AR5_all_final":"counts_WG1AR5_all_final_parsed",
        "SREX_Full_Report-1":"counts_SREX_Full_Report-1_parsed",
        "SRREN_Full_Report-1":"counts_SRREN_Full_Report-1_parsed",
        "ar4_syr_full_report":"counts_ar4_syr_full_report_parsed",
        "ar4_wg2_full_report":"counts_ar4_wg2_full_report_parsed",
        "ar4_wg1_full_report-1":"counts_ar4_wg1_full_report-1_parsed",
        "ar4_wg3_full_report-1":"counts_ar4_wg3_full_report-1_parsed",
        "sroc_full-1":"counts_sroc_full-1_parsed",
        "srccs_wholereport-1":"counts_srccs_wholereport-1_parsed",
        "SYR_TAR_full_report":"counts_SYR_TAR_full_report_parsed",
        "WGII_TAR_full_report-2":"counts_WGII_TAR_full_report-2_parsed",
        "WGI_TAR_full_report":"counts_WGI_TAR_full_report_parsed",
        "WGIII_TAR_full_report":"counts_WGIII_TAR_full_report_parsed",
        "srl-en-1":"counts_srl-en-1_parsed",
        "srtt-en-1":"counts_srtt-en-1_parsedd",
        "emissions_scenarios-1":"counts_emissions_scenarios-1_parsed",
        "av-en-1":"counts_av-en-1_parsed",
        "The-Regional-Impact":"counts_The-Regional-Impact_parsed",
        "2nd-assessment-en-1":"counts_2nd-assessment-en-1_parsed",
        "ipcc_sar_wg_III_full_report":"counts_ipcc_sar_wg_III_full_report_parsed",
        "ipcc_sar_wg_II_full_report":"counts_ipcc_sar_wg_II_full_report_parsed",
        "ipcc_sar_wg_I_full_report":"counts_ipcc_sar_wg_I_full_report_parsed",
        "climate_change_1994-2":"counts_climate_change_1994-2_parsed",
       # "ipcc-technical-guidelines-1994n-1":"", # could not read in, but also contains no temp mentions
        "ipcc_wg_I_1992_suppl_report_full_report":"counts_ipcc_wg_I_1992_suppl_report_full_report_parsed",
        "ipcc_wg_II_1992_suppl_report_full_report":"counts_ipcc_wg_II_1992_suppl_report_full_report_parsed",
        "ipcc_90_92_assessments_far_full_report":"counts_ipcc_90_92_assessments_far_full_report_parsed",
        "ipcc_far_wg_III_full_report":"counts_ipcc_far_wg_III_full_report_parsed",
        "ipcc_far_wg_II_full_report":"counts_ipcc_far_wg_II_full_report_parsed",
        "ipcc_far_wg_I_full_report":"counts_ipcc_far_wg_I_full_report_parsed",
        }
    return lookup_dict


def create_temp_keys():
    """Creates a list of strings for all temperatures the paper looked at"""
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
