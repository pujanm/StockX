#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 01:54:22 2018

@author: pujan
"""

import pandas as pd
import numpy as np
from numpy import nan as Nan
f = pd.read_csv("StockNews.csv")
d = pd.read_csv("Data.csv")

X = d.iloc[:, 0]
y = d.iloc[:, 1]
f = pd.DataFrame(Nan, index=range(0, 63),columns=['Date', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
Z = X.drop_duplicates(keep='first')
#f.iloc[9, 0]
for i in range(0, 63):
    f.iloc[i, 0] = Z.iloc[i]

k=0
for j in range(0, 63):
    for i in range(1, 11):
       f.iloc[j, i] = y.iloc[k]
       k += 1     
data1 = pd.read_csv("final.csv")
"""
d = np.array(d, dtype='str')
for i in range(0, 640):
    print(d[i][0])
    print(d[i][1])
    news.append(d[i][0])

news"""