# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 10:12:26 2021

@author: Florian Jehn
"""
import os
import pandas as pd
import numpy as np
import re
import random


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


def read_false_positive():
    """reads in all the counted false/true positive rates for the temperatres in the
        IPCC and calculates a true positive rate for each entry"""
    files = os.listdir(os.getcwd()+os.sep+"Results"+ os.sep + "false_positive_check_files")
    all_df = pd.DataFrame()
    for file in files:
        # only read those files that contains the counting results
        if "results" not in file:
            continue
        file_df = pd.read_csv("Results" + os.sep + "false_positive_check_files" + os.sep + file, sep=",", index_col=0)
        # calculate the true positive rate
        file_df["True Positive Rate [%]"] = (file_df["n true positive"]/(file_df["n true positive"]+file_df["n false positive"]))*100
        # Arange the df for seaborn
        file_df["Temperature [°C]"] = file_df.index
        file_df.reset_index(inplace=True, drop=True)
        all_df = pd.concat([all_df, file_df])
    return all_df        


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
    ipcc_counts["0.5°C - 2°C"] = ipcc_counts[" 0.5°C"] + ipcc_counts[" 1°C"] + ipcc_counts[" 1.5°C"] +ipcc_counts[" 2°C"] 
    ipcc_counts["2.5°C - 4°C"] = ipcc_counts[" 2.5°C"] + ipcc_counts[" 3°C"] + ipcc_counts[" 3.5°C"] +ipcc_counts[" 4°C"] 
    ipcc_counts["≥ 4.5°C"] = ipcc_counts[" 4.5°C"] + ipcc_counts[" 5°C"] + ipcc_counts[" 5.5°C"] +ipcc_counts[" 6°C"] +ipcc_counts[" 6.5°C"] + ipcc_counts[" 7°C"] + ipcc_counts[" 7.5°C"] +ipcc_counts[" 8°C"] + ipcc_counts[" 8.5°C"] + ipcc_counts[" 9°C"] + ipcc_counts[" 9.5°C"] +ipcc_counts[" 10°C"] 
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
    reports = [file for file in os.listdir(os.getcwd() + os.sep + "Raw IPCC Strings") if file[-4:] == ".csv" ]
    all_reports = " "
    for report in reports:       
        print("Starting with " + report) 
        report_df = pd.read_csv(os.getcwd() + os.sep + "Raw IPCC Strings" + os.sep + report, sep="\t", usecols=[0])
        report_list = report_df[report_df.columns[0]].tolist()
        report_str = " ".join([str(item) for item in report_list])
        all_reports += report_str
    
    with open(os.getcwd() + os.sep + "Raw IPCC Strings" + os.sep + "all_ipcc_strings.csv", 'w', encoding='utf-8') as f:
        # this file is not included in the repository, as it is too large for Github
        f.write(all_reports)


def create_temp_dict():
    """Creates a dictionary for all the single temperatures to count and returns it"""
    temp_dict = {}
    for i in np.arange(0.5,10.5, 0.5):
        # Test if it is a float or not to format it right
        if i == int(i):
            # Add an empty space at the beginnign to make sure this is not counting e.g. 1.5°C  as 5°C
            key = " " + str(int(i)) + "°C"
        else: 
            key = " " + str(i )+ "°C"
        temp_dict[key] = 0
    return temp_dict
    

def get_all_string(report):
    with open(os.getcwd() + os.sep + "Raw IPCC Strings" + os.sep + report, 'r', encoding='utf-8') as f:
        return f.read()
    

def count_temperatures(report):
    """counts all temperatures between 0.5°C and 10°C in 0.5°C steps"""
    temp_dict = create_temp_dict()
    report_df = pd.read_csv(os.getcwd() + os.sep + "Raw IPCC Strings" + os.sep + report, sep="\t", usecols=[0])
    report_list = report_df[report_df.columns[0]].tolist()
    report_str = " ".join([str(item) for item in report_list])
    # count how often a temperature occures
    for temp in temp_dict.keys():
        number_of_occurences = report_str.count(temp)
        print("Found " + temp +  " " + str(number_of_occurences) + " time(s)")
        temp_dict[temp] += number_of_occurences
    # Save the results for the single pdf
    temp_counts_pdf = pd.DataFrame.from_dict(temp_dict, orient="index")
    temp_counts_pdf.to_csv("Results" + os.sep + "temperatures" + os.sep + "counts_" + report[:-4] + ".csv", sep=";")
    
    
def count_temp_in_all_reports():
    """iterates over all reports"""
    reports = [file for file in os.listdir(os.getcwd() + os.sep + "Raw IPCC Strings") if file[-4:] == ".csv" ]
    for report in reports:
        print("Starting with " + report)  
        count_temperatures(report)    


def create_rfc_dict():
    """Creates a dictionary for all "reasons for concern" to count and returns it"""
    rfc_dict = {
        "unique and threatened systems":0,
        "extreme climate events":0,
        "distribution of impacts":0,
        "aggregate impacts":0,
        "large-scale singular event":0
        }
    return rfc_dict
    

def count_rfc(report):
    """counts all reasons of concerns mentioned in a given report"""
    rfc_dict = create_rfc_dict()
    report_df = pd.read_csv(os.getcwd() + os.sep + "Raw IPCC Strings" + os.sep + report, sep="\t", usecols=[0])
    report_list = report_df[report_df.columns[0]].tolist()
    report_str = " ".join([str(item) for item in report_list])
    # count how often a temperature occures
    for reason_for_concern in rfc_dict.keys():
        number_of_occurences = report_str.count(reason_for_concern)
        print("Found " + reason_for_concern +  " " + str(number_of_occurences) + " time(s)")
        rfc_dict[reason_for_concern] += number_of_occurences
    # Save the results for the single pdf
    rfc_counts_pdf = pd.DataFrame.from_dict(rfc_dict, orient="index")
    rfc_counts_pdf.to_csv("Results" + os.sep + "reasons_for_concern" + os.sep + "counts_" + report[:-4] + ".csv", sep=";")
     
    
def count_rfc_in_all_reports():
    """iterates over all reports"""
    reports = [file for file in os.listdir(os.getcwd() + os.sep + "Raw IPCC Strings") if file[-4:] == ".csv" ]
    for report in reports:
        print("Starting with " + report)  
        count_rfc(report)
        

def read_ipcc_string():
    """reads in the string that contains all reports"""
    with open(os.getcwd() + os.sep + "Raw IPCC Strings" + os.sep + "all_ipcc_strings.csv", 'r', encoding='utf-8') as f:
        return str(f.readlines())
    
    
def find_all_temp_occurence(ipcc_string):
    """finds all occurences for all temperatures"""
    temp_dict = {}
    for i in [1,1.5,2,3,4,5,6,7,8,9,10]:
        # Test if it is a float or not to format it right
        if i == int(i):
            # Add an empty space at the beginnign to make sure this is not counting e.g. 1.5°C  as 5°C
            key = " " + str(int(i)) + "°C"
        else: 
            key = " " + str(i)+ "°C"
        temp_dict[key] = [m.start() for m in re.finditer(key, ipcc_string)]
    return temp_dict
    

def get_strings_around_temps(temp_dict, ipcc_string, n_temp_sample=10, sample_length=250):
    """extracts the text around a given index in the string of all ipcc reports"""
    # number of files created with independent samples
    amount_files = 6
    for file in range(amount_files):
        with open(os.getcwd() + os.sep + "Results" + os.sep + "false_positive_check_files" + os.sep + "false_positive_"+str(file+1)+".csv", 'w', encoding='utf-8') as f:       
            for temp in temp_dict.keys():
                random_temp_sample = random.sample(temp_dict[temp],n_temp_sample)
                for index in random_temp_sample:
                    f.write(ipcc_string[int(index-(sample_length/2)):int(index+(sample_length/2))]+"\n\n")
            

if __name__ == "__main__":
    # Run the data analysis
    combine_all_raw_strings()
    count_rfc_in_all_reports()
    count_temp_in_all_reports()

    # Get the random sample
    ipcc_string = read_ipcc_string()
    temp_dict = find_all_temp_occurence(ipcc_string)
    random.seed(1)
    get_strings_around_temps(temp_dict, ipcc_string)