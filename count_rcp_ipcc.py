# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:56:42 2020

@author: Florian Jehn
"""
import re
import numpy as np
import pandas as pd
import os
import csv

def create_rcp_dict():
    """Creates a dictionary for all "reasons for concern" to count and returns it"""
    rcp_dict = {
        "RCP2.6":0,
        "RCP4.5":0,
        "RCP6.0":0,
        "RCP8.5":0,
        }
    return rcp_dict
    

def get_all_string(report):
    with open(os.getcwd() + os.sep + "Raw IPCC Strings" + os.sep + report, 'r', encoding='utf-8') as f:
        return f.read()
    

def count_rcp(report):
    rcp_dict = create_rcp_dict()
    report_df = pd.read_csv(os.getcwd() + os.sep + "Raw IPCC Strings" + os.sep + report)
    # make sure everything is in one column
    if len(report_df.columns) != 1:
        print(report)
        raise TypeError("Should be a dataframe with only one column")
    # count how often a temperature occures
    for reason_for_concern in rcp_dict.keys():
        number_of_occurences = report_df[report_df.columns[0]].str.count(reason_for_concern).sum() 
        print("Found " + reason_for_concern +  " " + str(number_of_occurences) + " time(s)")
        rcp_dict[reason_for_concern] += number_of_occurences
    # Save the results for the single pdf
    rcp_counts_pdf = pd.DataFrame.from_dict(rcp_dict, orient="index")
    rcp_counts_pdf.to_csv("Results" + os.sep + "rcps" + os.sep + "counts_" + report[:-4] + ".csv", sep=";")
    
        
    
def count_all_reports():
    reports = [file for file in os.listdir(os.getcwd() + os.sep + "Raw IPCC Strings") if file[-4:] == ".csv" ]
    for report in reports:
        print("Starting with " + report)  
        count_rcp(report)

if __name__ == "__main__":  
    # Counts all reasons for concern and saves it as files. 
    count_all_reports()
