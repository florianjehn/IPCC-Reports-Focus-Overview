# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:32:12 2020

@author: Florian Jehn
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import read_prepare_data as rp_da


def plot_all_temp_by_ar(ipcc_counts, meta, cmap):
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
    ax = counts_meta.groupby("AR")[temps].mean().plot(cmap=cmap, kind="bar", width=1, stacked=True)    
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1],loc='upper right', bbox_to_anchor=(1.15, 1))
    # Plot the temp groups
    temp_group_means_by_ar = counts_meta.groupby("AR")[temp_groups].mean()
    # prep df for stacking
    temp_group_means_by_ar["2.5°C-4°C"] = temp_group_means_by_ar["2.5°C-4°C"] + temp_group_means_by_ar["0.5°C-2°C"]
    del(temp_group_means_by_ar["≥4.5°C"])
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
                
    for temp_group, y_pos in zip(temp_groups, [20,58,85]):
        ax.text(2, y_pos,temp_group, fontsize=20, fontweight="bold")
        
    # Make pretty
    ax.set_ylabel("% Mentions")
    fig = plt.gcf()
    fig.set_size_inches(10,10)
    fig.tight_layout()
    plt.savefig("Figures"+ os.sep +"AR_all_temps_and_grouped.png", dpi=200)
    plt.close()
    return counts_meta

if __name__ == "__main__":
    # Define basic stuff
    # exclude reports with only few temperature mentions, as they distort the picture
    min_temp_found = 10
    cmap = "magma_r"
    
    # get the data    
    ipcc_counts = rp_da.read_ipcc_counts_temp()

    meta = rp_da.read_meta()
    # Get the other file names to be able to merge later
    meta["count_names"] = meta["PDF Name"].map(rp_da.lookup_names())
    
    # Remove the ones with few entries overall
    ipcc_counts = ipcc_counts[ipcc_counts.sum(axis=1)>min_temp_found]
    
    # Plot    
    counts_meta= plot_all_temp_by_ar(ipcc_counts, meta, cmap)

    
    
    
    
    

