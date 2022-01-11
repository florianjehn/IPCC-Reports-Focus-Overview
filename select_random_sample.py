# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 14:08:41 2022

@author: Florian Jehn
"""
import pandas as pd
import os
import random
import re
import numpy as np


def read_ipcc_string():
    """reads in the string that contains all reports"""
    with open(os.getcwd() + os.sep + "Raw IPCC Strings" + os.sep + "all_ipcc_strings.csv", 'r', encoding='utf-8') as f:
        return str(f.readlines())
    
    
def find_all_temp_occurence(ipcc_string):
    """finds all occurences for all temperatures"""
    temp_dict = {}
    for i in np.arange(1,10.5, 1):
        # Test if it is a float or not to format it right
        if i == int(i):
            # Add an empty space at the beginnign to make sure this is not counting e.g. 1.5°C  as 5°C
            key = " " + str(int(i)) + "°C"
        else: 
            key = " " + str(i )+ "°C"
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
    ipcc_string = read_ipcc_string()
    temp_dict = find_all_temp_occurence(ipcc_string)
    random.seed(1)
    get_strings_around_temps(temp_dict, ipcc_string)
    
    
    


