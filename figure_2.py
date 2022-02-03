# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 17:14:42 2022

@author: Florian Jehn
"""

import matplotlib.pyplot as plt
import os
import read_prepare_data as rp_da
import seaborn as sns
import pandas as pd


def plot_nicer(ax):
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
    plot_nicer(ax)
    fig = plt.gcf()
    fig.set_size_inches(8,2.2)
    fig.tight_layout()
    plt.savefig("Figures"+ os.sep +"true_positive_rate.png", dpi=200)
    plt.close()
    

if __name__ == "__main__":
    tp_rate = rp_da.read_false_positive()
    plot_tp_rate(tp_rate)
