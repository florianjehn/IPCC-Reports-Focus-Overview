# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:56:42 2020

@author: Florian Jehn
"""
import pandas as pd
import os


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
     
    
def count_all_reports():
    """iterates over all reports"""
    reports = [file for file in os.listdir(os.getcwd() + os.sep + "Raw IPCC Strings") if file[-4:] == ".csv" ]
    for report in reports:
        print("Starting with " + report)  
        count_rfc(report)
        

if __name__ == "__main__":  
    # Counts all reasons for concern and saves it as files. 
    count_all_reports()
