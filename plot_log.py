# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 08:42:49 2022

@author: vollmera
"""
import pandas as pd
import os
import matplotlib.pyplot as plt

folder="C:\\Users\\vollmera\\Documents\\SVN_home\\trunk\\SW_app\\github\\Rasp2Cloud\\log_data\\"
dirs=os.listdir(folder)


for each in dirs:
    mdf=pd.read_csv(folder+str(each))
    plt.plot(mdf)
    plt.show()