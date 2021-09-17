# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:32:12 2020

@author: Florian Jehn
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import read_prepare_data as rp_da


def plot_all_temp_by_ar(ipcc_counts, meta):
    """Plots all temperatures for all assessment reports  """
    ipcc_counts = rp_da.scale_counts(ipcc_counts.copy())
    # group for second layer of plot
    ipcc_counts_grouped = rp_da.group_temps(ipcc_counts.copy())
    temp_groups =  ipcc_counts_grouped.columns
    # prep for plotting
    counts_meta = rp_da.merge_counts_meta(ipcc_counts, meta)
    counts_meta = rp_da.merge_counts_meta(ipcc_counts_grouped, counts_meta)
    temps = rp_da.create_temp_keys()
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
    
def plot_all_temp_by_wg(ipcc_counts, meta):
    """Plots all temperatures for all assessment reports  """
    ipcc_counts = rp_da.scale_counts(ipcc_counts.copy())
    # group for second layer of plot
    ipcc_counts_grouped = rp_da.group_temps(ipcc_counts.copy())
    temp_groups =  ipcc_counts_grouped.columns
    # prep for plotting
    counts_meta = rp_da.merge_counts_meta(ipcc_counts, meta)
    counts_meta = rp_da.merge_counts_meta(ipcc_counts_grouped, counts_meta)
    temps = rp_da.create_temp_keys()
    
    wgI = counts_meta[counts_meta["Working Group I"] == True]
    wgII = counts_meta[counts_meta["Working Group II"] == True]
    wgIII = counts_meta[counts_meta["Working Group III"] == True]

    wgs_continous_temp = pd.concat([wgI[temps].mean(), wgII[temps].mean(), wgIII[temps].mean()],axis=1)
    wgs_continous_temp.columns = ["WG I", "WG II", "WG III"]
    wgs_continous_temp = wgs_continous_temp.transpose()
    # Plot the working groups
    ax = wgs_continous_temp.plot(cmap="coolwarm", kind="bar", width=0.9, stacked=True)
    # Handle the legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1],loc='upper right', bbox_to_anchor=(1.15, 1))
    # Plot the temp groups
    wgs_group_temp = pd.concat([wgI[temp_groups].mean(), wgII[temp_groups].mean(), wgIII[temp_groups].mean()],axis=1)
    wgs_group_temp.columns = ["WG I", "WG II", "WG III"]
    wgs_group_temp = wgs_group_temp.transpose()
    # prep df for stacking
    wgs_group_temp["2.5°C-4°C"] = wgs_group_temp["2.5°C-4°C"] + wgs_group_temp["0.5°C-2°C"]
    del(wgs_group_temp[">=4.5°C"])
    # plot  group lines
    for temp_group in temp_groups[:-1]:
        for i, WG in enumerate(wgs_group_temp[temp_group]):
            # plot horizontal line
            ax.plot([i-0.45,i+1-0.55], [WG,WG], color="black")


    for temp_group, y_pos in zip(temp_groups, [20,60,90]):
        ax.text(0.7, y_pos,temp_group, fontsize=20, fontweight="bold")
        
    # Make pretty
    ax.set_ylabel("% Mentions")
    fig = plt.gcf()
    fig.set_size_inches(10,10)
    fig.tight_layout()
    plt.savefig("Figures"+ os.sep +"WG_all_temps_and_grouped.png", dpi=200)
    plt.close()
    
def plot_all_temp_by_report_type(ipcc_counts, meta):
    """Plots all temperatures for all assessment reports  """
    ipcc_counts = rp_da.scale_counts(ipcc_counts.copy())
    # group for second layer of plot
    ipcc_counts_grouped = rp_da.group_temps(ipcc_counts.copy())
    temp_groups =  ipcc_counts_grouped.columns
    # prep for plotting
    counts_meta = rp_da.merge_counts_meta(ipcc_counts, meta)
    counts_meta = rp_da.merge_counts_meta(ipcc_counts_grouped, counts_meta)
    temps = rp_da.create_temp_keys()
    # Plot the seperate temps
    ax = counts_meta.groupby("Kind of Report")[temps].mean().plot(cmap="coolwarm", kind="bar", width=0.9, stacked=True)    
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1],loc='upper right', bbox_to_anchor=(1.15, 1))
    # Plot the temp groups
    temp_group_means_by_report = counts_meta.groupby("Kind of Report")[temp_groups].mean()
    # prep df for stacking
    temp_group_means_by_report["2.5°C-4°C"] = temp_group_means_by_report["2.5°C-4°C"] + temp_group_means_by_report["0.5°C-2°C"]
    del(temp_group_means_by_report[">=4.5°C"])
    # plot  group lines
    for temp_group in temp_groups[:-1]:
        for i, AR in enumerate(temp_group_means_by_report[temp_group]):
            # plot horizontal line
            ax.plot([i-0.45,i+1-0.55], [AR,AR], color="black")
            # Plot vertical lines


    for temp_group, y_pos in zip(temp_groups, [20,60,90]):
        ax.text(1.6, y_pos,temp_group, fontsize=20, fontweight="bold")
        
    # Make pretty
    ax.set_ylabel("% Mentions")
    fig = plt.gcf()
    fig.set_size_inches(10,10)
    fig.tight_layout()
    plt.savefig("Figures"+ os.sep +"report_type_all_temps_and_grouped.png", dpi=200)
    plt.close()
    
    
if __name__ == "__main__":
    # Define basic stuff
    min_temp_found = 5
    
    # get the data    
    ipcc_counts = rp_da.read_ipcc_counts()

    meta = rp_da.read_meta()
    # Get the other file names to be able to merge later
    meta["count_names"] = meta["PDF Name"].map(rp_da.lookup_names())
    
    # Remove the ones with few entries overall
    ipcc_counts = ipcc_counts[ipcc_counts.sum(axis=1)>min_temp_found]
    
    # Plot    
   # plot_all_temp_by_ar(ipcc_counts, meta)
    plot_all_temp_by_wg(ipcc_counts, meta)

    plot_all_temp_by_report_type(ipcc_counts, meta)
    # TODO
    # exclude reports with fewer than 10 entries?
    
    
    
    
    
    

