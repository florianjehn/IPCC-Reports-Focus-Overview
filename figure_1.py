# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:32:12 2020

@author: Florian Jehn
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


def plot_nicer(ax, with_legend=True):
    """Takes an axis objects and makes it look nicer"""
    alpha=0.7
    for spine in ax.spines.values():
      spine.set_color("lightgray")
    # Make text grey
    plt.setp(ax.get_yticklabels(), alpha=alpha)
    plt.setp(ax.get_xticklabels(), alpha=alpha)
    ax.set_xlabel(ax.get_xlabel(), alpha=alpha)
    ax.set_ylabel(ax.get_ylabel(), alpha=alpha)
    ax.set_title(ax.get_title(), alpha=alpha)
    ax.tick_params(axis=u'both', which=u'both',color="#676767")
    if with_legend:
      legend = ax.get_legend()
      for text in legend.get_texts():
        text.set_color("#676767")
      legend.get_title().set_color("#676767")
    ax.yaxis.get_offset_text().set_color("#676767")


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
    ipcc_counts[">=4.5°C"] = ipcc_counts[" 4.5°C"] + ipcc_counts[" 5°C"] + ipcc_counts[" 5.5°C"] +ipcc_counts[" 6°C"] +ipcc_counts[" 6.5°C"] + ipcc_counts[" 7°C"] + ipcc_counts[" 7.5°C"] +ipcc_counts[" 8°C"] + ipcc_counts[" 8.5°C"] + ipcc_counts[" 9°C"] + ipcc_counts[" 9.5°C"] +ipcc_counts[" 10°C"] 
    return ipcc_counts.iloc[:,20:]
    

def merge_counts_meta(ipcc_counts, meta):
    return pd.merge(meta, ipcc_counts, right_index=True, left_on="count_names") 


def plot_all_temp_by_ar(ipcc_counts, meta):
    """Plots all temperatures for all assessment reports  """
    ipcc_counts = scale_counts(ipcc_counts.copy())
    # group for second layer of plot
    ipcc_counts_grouped = group_temps(ipcc_counts.copy())
    temp_groups =  ipcc_counts_grouped.columns
    # prep for plotting
    counts_meta = merge_counts_meta(ipcc_counts, meta)
    counts_meta = merge_counts_meta(ipcc_counts_grouped, counts_meta)
    temps = create_temp_keys()
    # Plot the seperate temps
    ax = counts_meta.groupby("AR")[temps].mean().plot(cmap="coolwarm", kind="bar", width=1, stacked=True)    
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1],loc='upper right', bbox_to_anchor=(1.15, 1))
    # Plot the temp groups
    temp_group_means_by_ar = counts_meta.groupby("AR")[temp_groups].mean()
    # prep df for stacking
    temp_group_means_by_ar["2.5°C-4°C"] = temp_group_means_by_ar["2.5°C-4°C"] + temp_group_means_by_ar["0.5°C-2°C"]
    del(temp_group_means_by_ar[">=4.5°C"])
    # plot  group lines
    for temp_group in temp_groups[:-1]:
        last_AR = 0
        for i, AR in enumerate(temp_group_means_by_ar[temp_group]):
            # plot horizontal line
            ax.plot([i-0.5,i+1-0.5], [AR,AR], color="black")
            # Plot vertical lines
            if i > 0:
                ax.plot([i-0.5, i-0.5], [AR, last_AR], color="black")    
                last_AR = AR
            else:
                last_AR = AR

    for temp_group, y_pos in zip(temp_groups, [20,60,90]):
        ax.text(2, y_pos,temp_group, fontsize=20, fontweight="bold")
        
    # Make pretty
    ax.set_ylabel("% Mentions")
    fig = plt.gcf()
    fig.set_size_inches(10,10)
    fig.tight_layout()
    plt.savefig("Figures"+ os.sep +"AR_all_temps_and_grouped.png", dpi=200)
    plt.close()
    

def create_temp_keys():
    temps = []
    for i,temp in enumerate(np.arange(0.5,10.1,0.5)):
        if i % 2 != 0:
             temps.append(" "+str(int(temp))+"°C")
        else: 
             temps.append(" "+str(temp)+"°C" )
    return temps


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
    
#ReportsWGIIITARfullreportpdf_parsed
if __name__ == "__main__":
    # Define basic stuff
    min_temp_found = 5
    
    # get the data    
    ipcc_counts = read_ipcc_counts()

    meta = read_meta()
    # Get the other file names to be able to merge later
    meta["count_names"] = meta["PDF Name"].map(lookup_names())
    
    # Remove the ones with few entries overall
    ipcc_counts = ipcc_counts[ipcc_counts.sum(axis=1)>min_temp_found]
    
    # Plot    
    plot_all_temp_by_ar(ipcc_counts, meta)


    # TODO
    # exclude reports with fewer than 10 entries?
    
    
    
    
    
    

