# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 13:47:40 2021

@author: Florian Jehn
"""
import os
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

df =  pd.read_csv("Raw IPCC Strings" + os.sep + "all_reports.csv")
df["merged"] = df[df.columns[1:]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)
df = df["merged"]
text = df.str.cat(sep=" ")
wordcloud = WordCloud().generate(text)

plt.imshow(wordcloud, interpolation="bilinear")
plt.savefig("Figures" + os.sep + "word_cloud.png",dpi=300)
plt.show()