# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:56:42 2020

@author: Florian Jehn
"""
import numpy as np
import pandas as pd
import os


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
    
    
def count_all_reports():
    """iterates over all reports"""
    reports = [file for file in os.listdir(os.getcwd() + os.sep + "Raw IPCC Strings") if file[-4:] == ".csv" ]
    for report in reports:
        print("Starting with " + report)  
        count_temperatures(report)
        

count_all_reports()
