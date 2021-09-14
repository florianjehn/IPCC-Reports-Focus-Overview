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



# def read_counts_total():
#     # Read in the data
#     ipcc_counts = pd.read_csv("Results" + os.sep + "temp_counts_all.csv", sep=";", index_col=0)
    
#     # Replace the spaces in the temperature description
#     ipcc_counts.index = ipcc_counts.index.str.replace(" ","")
#     # Make temperatures numerical
#     ipcc_counts.index = ipcc_counts.index.str.replace("°C","")
#     ipcc_counts.reset_index(inplace=True)
#     ipcc_counts.columns=["Temp Rise", "Count"]
#     ipcc_counts["Temp Rise"] = ipcc_counts["Temp Rise"].astype(float)
#     return ipcc_counts

def read_ipcc_counts():
    """reads all counts for all reports and makes on df"""
    files = os.listdir(os.getcwd()+os.sep+"Results")
    all_df = pd.DataFrame()
    for file in files:
        # skip the total counts for now
        if file == 'temp_counts_all.csv':
            continue
        file_df = pd.read_csv("Results" + os.sep + file, sep=";", index_col=0)
        file_df.columns = [file[7:-4]]
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
    meta = pd.read_csv("Reports" + os.sep + "meta_data_reports.tsv", sep="\t", index_col=-1)
    meta["Year"]  = meta["Year"].astype("str")
    return meta

def group_temps(ipcc_counts):
    ipcc_counts["0.5°C-2°C"] = ipcc_counts[" 0.5°C"] + ipcc_counts[" 1°C"] + ipcc_counts[" 1.5°C"] +ipcc_counts[" 2°C"] 
    ipcc_counts["2.5°C-4°C"] = ipcc_counts[" 2.5°C"] + ipcc_counts[" 3°C"] + ipcc_counts[" 3.5°C"] +ipcc_counts[" 4°C"] 
    ipcc_counts[">=4.5°C"] = ipcc_counts[" 4.5°C"] + ipcc_counts[" 5°C"] + ipcc_counts[" 5.5°C"] +ipcc_counts[" 6°C"] +ipcc_counts[" 6.5°C"] + ipcc_counts[" 7°C"] + ipcc_counts[" 7.5°C"] +ipcc_counts[" 8°C"] + ipcc_counts[" 8.5°C"] + ipcc_counts[" 9°C"] + ipcc_counts[" 9.5°C"] +ipcc_counts[" 10°C"] 
    return ipcc_counts.iloc[:,20:]
    

def merge_counts_meta(ipcc_counts, meta):
    return pd.merge(meta, ipcc_counts, right_index=True, left_index=True) 

def plot_all_temp_by_ar(ipcc_counts, meta):
    """Plots all temperatures for all assessment reports  """
    ipcc_counts = scale_counts(ipcc_counts.copy())
    # group for second layer of plot
    ipcc_counts_grouped = group_temps(ipcc_counts.copy())
    temp_groups =  ipcc_counts_grouped.columns
    # prep for plotting
    counts_meta = merge_counts_meta(ipcc_counts, meta)
    counts_meta = merge_counts_meta(counts_meta, ipcc_counts_grouped)
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
    
def plot_group_temp_by_ar(ipcc_counts, meta):
    """Plots all temperatures for all assessment reports  """
    ipcc_counts = group_temps(ipcc_counts.copy())
    temps=ipcc_counts.columns
    ipcc_counts = scale_counts(ipcc_counts.copy())
    counts_meta = merge_counts_meta(ipcc_counts, meta)
    ax = counts_meta.groupby("AR")[temps].mean().plot(cmap="coolwarm", kind="bar", width=1, stacked=True)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1],loc='upper right', bbox_to_anchor=(1.15, 1))
    ax.set_ylabel("% Mentions")
    fig = plt.gcf()
    fig.set_size_inches(10,10)
    fig.tight_layout()
    plt.savefig("Figures"+ os.sep +"AR_group_temps.png", dpi=200)    
    plt.close()

def create_temp_keys():
    temps = []
    for i,temp in enumerate(np.arange(0.5,10.1,0.5)):
        if i % 2 != 0:
             temps.append(" "+str(int(temp))+"°C")
        else: 
             temps.append(" "+str(temp)+"°C" )
    return temps


if __name__ == "__main__":
    # Define basic stuff
    color_prob = "#4F4F4F"
    color_count = "#DBB587"
    edgecolor = "white"
    min_temp_found = 5
    # get the data
    meta = read_meta()

    ipcc_counts = read_ipcc_counts()
    # Remove the ones with few entries overall
    ipcc_counts = ipcc_counts[ipcc_counts.sum(axis=1)>min_temp_found]
    
    
   # ipcc_counts_grouped = group_temps(ipcc_counts.copy())
  #  ipcc_counts_grouped = 
   # ipcc_counts_scaled = scale_counts(ipcc_counts_grouped.copy())
    
    plot_all_temp_by_ar(ipcc_counts, meta)
#    plot_group_temp_by_ar(ipcc_counts, meta)
    # # WG plotting
    # fig, axes = plt.subplots(nrows=3,sharey=True, sharex=True)
    # axes.flatten()
    # wg1 = meta_and_counts[meta_and_counts["Working Group I"]]
    # wg1.iloc[:,-3:].mean().plot(kind="bar", ax=axes[0])
    # axes[0].set_title("WG1")
    # wg2 = meta_and_counts[meta_and_counts["Working Group II"]]
    # wg2.iloc[:,-3:].mean().plot(kind="bar", ax=axes[1]) 
    # axes[1].set_title("WG2")
    # wg3 = meta_and_counts[meta_and_counts["Working Group III"]]
    # wg3.iloc[:,-3:].mean().plot(kind="bar", ax=axes[2])
    # axes[2].set_title("WG3")    
    # for ax in axes:
    #     ax.set_ylabel("% Mentions")
    #     ax.yaxis.grid(True)
    # fig.tight_layout()
    # plt.savefig("WG.png", dpi=200)
    # #plt.close()
    
    
    
    # # Remove for plotting   
    # del(meta_and_counts["Working Group I"])
    # del(meta_and_counts["Working Group II"])
    # del(meta_and_counts["Working Group III"])
    
    # # AR plotting
    # 
    

    # TODO
    # why meta_coutns only 36 long?
    # exclude reports with fewer than 10 entries?
    
    
    
    
    
    

