# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 10:25:32 2022

@author: vollmera
"""
import time
abc=time.gmtime()

print(abc)


len(abc)
dateTimeRow=""
for each in range(len(abc)):
    dateTimeRow+=str(abc[each])+"_"
dateTimeRow=dateTimeRow[:-1]
print(dateTimeRow)


import pandas as pd
import matplotlib.pyplot as plt
mdf=pd.read_csv("2022_February_23_104650.csv")
plt.plot(mdf)