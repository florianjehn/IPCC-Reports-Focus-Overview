# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 11:56:56 2021

@author: Florian Jehn
"""


import pandas as pd
import matplotlib.pyplot as plt
import os
import read_prepare_data as rp_da
import count_rcp_ipcc

def plot_all_rcp_by_ar(ipcc_counts, meta, cmap):
    """Plots all temperatures for all assessment reports  """
    ipcc_counts = rp_da.scale_counts(ipcc_counts.copy())
    # prep for plotting
    counts_meta = rp_da.merge_counts_meta(ipcc_counts, meta)
    rcps = list(count_rcp_ipcc.create_rcp_dict().keys())
    # Plot the seperate temps
    ax = counts_meta.groupby("AR")[rcps].mean().plot(kind="bar", stacked=True, cmap=cmap)    

    # Make pretty
    ax.set_ylabel("% Mentions")
    fig = plt.gcf()
    fig.set_size_inches(10,10)
    fig.tight_layout()
    plt.savefig("Figures"+ os.sep +"AR_all_rcp_and_grouped.png", dpi=200)
    plt.close()

if __name__ == "__main__":
    # Define basic stuff
    # exclude reports with only few temperature mentions, as they distort the picture
    min_temp_found = 0
    cmap = "magma_r"
    
    # get the data    
    ipcc_counts = rp_da.read_ipcc_counts_rcp()

    meta = rp_da.read_meta()
    # Get the other file names to be able to merge later
    meta["count_names"] = meta["PDF Name"].map(rp_da.lookup_names())
    
    # Remove the ones with few entries overall
    ipcc_counts = ipcc_counts[ipcc_counts.sum(axis=1)>min_temp_found]
    
    # Plot    
    plot_all_rcp_by_ar(ipcc_counts, meta, cmap)