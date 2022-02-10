# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:44:22 2022

@author: vollmera
"""


import os
import os.path

dirList=os.listdir("/home/pi/Daq/files/")
print(dirList)
csvFile=[]
for each in dirList:
        if ".csv" in each:
                csvFile.append(each)
print(csvFile)

sendString='sudo  blobxfer upload --storage-account testbenchpi4 --sas "?sv=2020-08-04&ss=bfqt&srt=co&sp=rwdlacupitfx&se=2022-01-30T17:03:10Z&st=2022-01-19T09:03:10Z&spr=https&sig=ykOpTDsq5TjWQ22ntcqrvgkhGg%2F2%2FUeb3qUbIen6MAg%3D"--remote-path achimpi4 --local-path /home/pi/Daq/files/'

for all in csvFile:
        print(all)

        os.system(sendString+str(all))

