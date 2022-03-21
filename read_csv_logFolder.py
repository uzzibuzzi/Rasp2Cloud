#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 10:33:33 2022

@author: pi
"""

import pandas as pd
import os

folder="/home/pi/github/log_data/"
dirs=os.listdir(folder)

import matplotlib.pyplot as plt
mdf=pd.read_csv(folder+dirs[-1])

plt.plot(mdf)


plt.scatter(mdf.index,mdf[mdf.keys()[0]])