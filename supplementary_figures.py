# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 11:53:48 2021

@author: Florian Jehn
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
import read_prepare_data as rp_da
import seaborn as sns


def plot_all_temp_by_wg(ipcc_counts_temp, meta, cmap):
    """Plots all temperatures for all assessment reports  """
    ipcc_counts_temp = rp_da.scale_counts(ipcc_counts_temp.copy())
    # group for second layer of plot
    ipcc_counts_grouped_temp = rp_da.group_temps(ipcc_counts_temp.copy())
    temp_groups =  ipcc_counts_grouped_temp.columns
    # prep for plotting
    counts_meta = rp_da.merge_counts_meta(ipcc_counts_temp, meta)
    counts_meta = rp_da.merge_counts_meta(ipcc_counts_grouped_temp, counts_meta)
    temps = rp_da.create_temp_keys()
    
    wgI = counts_meta[counts_meta["Working Group I"] == True]
    wgII = counts_meta[counts_meta["Working Group II"] == True]
    wgIII = counts_meta[counts_meta["Working Group III"] == True]

    wgs_continous_temp = pd.concat([wgI[temps].mean(), wgII[temps].mean(), wgIII[temps].mean()],axis=1)
    wgs_continous_temp.columns = ["WG I", "WG II", "WG III"]
    wgs_continous_temp = wgs_continous_temp.transpose()
    # Plot the working groups
    ax = wgs_continous_temp.plot(cmap=cmap, kind="bar", width=0.9, stacked=True)
    # Handle the legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1],loc='upper right', bbox_to_anchor=(1.12, 0.962),labelspacing=1.4, frameon=False)
    # Plot the temp groups
    wgs_group_temp = pd.concat([wgI[temp_groups].mean(), wgII[temp_groups].mean(), wgIII[temp_groups].mean()],axis=1)
    wgs_group_temp.columns = ["WG I", "WG II", "WG III"]
    wgs_group_temp = wgs_group_temp.transpose()
    # prep df for stacking
    wgs_group_temp["2.5°C - 4°C"] = wgs_group_temp["2.5°C - 4°C"] + wgs_group_temp["0.5°C - 2°C"]
    del(wgs_group_temp["≥ 4.5°C"])
    # plot  group lines
    for temp_group in temp_groups[:-1]:
        for i, WG in enumerate(wgs_group_temp[temp_group]):
            # plot horizontal line
            ax.plot([i-0.45,i+1-0.55], [WG,WG], color="black")


    for temp_group, y_pos in zip(temp_groups, [20,60,90]):
        ax.text(0.7, y_pos,temp_group, fontsize=14, fontweight="bold")
        
    # Make pretty
    ax.set_ylabel("% Mentions")
    plot_nicer(ax)
    fig = plt.gcf()
    fig.set_size_inches(8,8)
    fig.tight_layout()
    plt.savefig("Figures"+ os.sep + "Supplementary" + os.sep + "WG_all_temps_and_grouped.png", dpi=200)
    plt.close()
    
    
def plot_all_temp_by_report_type(ipcc_counts_temp, meta, cmap):
    """Plots all temperatures for all assessment reports  """
    ipcc_counts_temp = rp_da.scale_counts(ipcc_counts_temp.copy())
    # group for second layer of plot
    ipcc_counts_grouped_temp = rp_da.group_temps(ipcc_counts_temp.copy())
    temp_groups =  ipcc_counts_grouped_temp.columns
    # prep for plotting
    counts_meta = rp_da.merge_counts_meta(ipcc_counts_temp, meta)
    counts_meta = rp_da.merge_counts_meta(ipcc_counts_grouped_temp, counts_meta)
    temps = rp_da.create_temp_keys()
    # Plot the seperate temps
    ax = counts_meta.groupby("Kind of Report")[temps].mean().plot(cmap=cmap, kind="bar", width=0.9, stacked=True)    
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1],loc='upper right', bbox_to_anchor=(1.12, 0.962),labelspacing=1.4, frameon=False)
    # Plot the temp groups
    temp_group_means_by_report = counts_meta.groupby("Kind of Report")[temp_groups].mean()
    # prep df for stacking
    temp_group_means_by_report["2.5°C - 4°C"] = temp_group_means_by_report["2.5°C - 4°C"] + temp_group_means_by_report["0.5°C - 2°C"]
    del(temp_group_means_by_report["≥ 4.5°C"])
    # plot  group lines
    for temp_group in temp_groups[:-1]:
        for i, AR in enumerate(temp_group_means_by_report[temp_group]):
            # plot horizontal line
            ax.plot([i-0.45,i+1-0.55], [AR,AR], color="black")
            # Plot vertical lines


    for temp_group, y_pos in zip(temp_groups, [20,60,90]):
        ax.text(1.6, y_pos,temp_group, fontsize=14, fontweight="bold")
        
    # Make pretty
    ax.set_ylabel("% Mentions")
    plot_nicer(ax)
    fig = plt.gcf()
    fig.set_size_inches(8,8)
    fig.tight_layout()
    plt.savefig("Figures"+ os.sep + "Supplementary" + os.sep + "report_type_all_temps_and_grouped.png", dpi=200)
    plt.close()
    
    
def plot_all_rfc_by_ar(ipcc_counts_rfc, meta, cmap):
    """Plots all reasons for concern for all assessment reports  """
    ipcc_counts_rfc = rp_da.scale_counts(ipcc_counts_rfc.copy())
    # prep for plotting
    counts_meta = rp_da.merge_counts_meta(ipcc_counts_rfc, meta)
    rfcs = list(rp_da.create_rfc_dict().keys())
    # Plot the seperate temps
    ax = counts_meta.groupby("AR")[rfcs].mean().plot(kind="bar", stacked=True, cmap=cmap)    
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc=7)
    # Make pretty
    ax.set_ylabel("% Mentions")
    plot_nicer(ax)
    fig = plt.gcf()
    fig.set_size_inches(8,8)
    fig.tight_layout()
    plt.savefig("Figures"+ os.sep + "Supplementary" + os.sep + "AR_all_rfc_and_grouped.png", dpi=200)
    plt.close()
    

def plot_nicer(ax, grid=False):
    """Takes an axis objects and makes it look nicer"""
    alpha=0.7
    for spine in ax.spines.values():
      spine.set_color("white")
    # Make text grey
    plt.setp(ax.get_yticklabels(), alpha=alpha)
    plt.setp(ax.get_xticklabels(), alpha=alpha)
    ax.set_xlabel(ax.get_xlabel(), alpha=alpha)
    ax.set_ylabel(ax.get_ylabel(), alpha=alpha)
    ax.set_title(ax.get_title(), alpha=alpha)
    if grid:
        ax.grid("lightgrey")
    ax.tick_params(axis=u'y', which=u'both',color="#676767")
    ax.tick_params(axis=u'x', which=u'both',color="#676767")
    

def plot_tp_rate(tp_rate):
    """Plots the false positive rate as a swarmplot with lines"""
    # Calculate the means for plotting
    means = pd.DataFrame(tp_rate.groupby("Temperature [°C]").mean()["True Positive Rate [%]"]).reset_index()
    ax = sns.swarmplot(y='True Positive Rate [%]',x="Temperature [°C]", data=means, palette="magma_r", edgecolor="black", linewidth=0.5)
    ax.plot(means["Temperature [°C]"].astype('str'), means["True Positive Rate [%]"], color="darkgrey")
    ax.set_ylim(0,100)
    # Make figure nicer
    plot_nicer(ax, grid=True)
    fig = plt.gcf()
    fig.set_size_inches(8,2.2)
    fig.tight_layout()
    plt.savefig("Figures"+ os.sep + "Supplementary" + os.sep + "true_positive_rate.png", dpi=200)
    plt.close()    
    
    
if __name__ == "__main__":
    # Define basic stuff
    # exclude reports with only few temperature mentions, as they distort the picture
    min_temp_found = 10
    cmap = "magma_r"
    
    # get the data    
    ipcc_counts_temp = rp_da.read_ipcc_counts_temp()
    ipcc_counts_rfc = rp_da.read_ipcc_counts_rfc()
    tp_rate = rp_da.read_false_positive()

    meta = rp_da.read_meta()
    # Get the other file names to be able to merge later
    meta["count_names"] = meta["PDF Name"].map(rp_da.lookup_names())
    
    # Remove the ones with few entries overall
    ipcc_counts_temp = ipcc_counts_temp[ipcc_counts_temp.sum(axis=1)>min_temp_found]
    ipcc_counts_rfc = ipcc_counts_rfc[ipcc_counts_rfc.sum(axis=1)>min_temp_found]
    
    # Plot    
    plot_all_temp_by_wg(ipcc_counts_temp, meta, cmap)
    plot_all_temp_by_report_type(ipcc_counts_temp, meta, cmap)
    plot_all_rfc_by_ar(ipcc_counts_rfc, meta, cmap)
    plot_tp_rate(tp_rate)