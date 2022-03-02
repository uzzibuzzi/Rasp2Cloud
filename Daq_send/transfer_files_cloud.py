# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 12:05:21 2022

@author: vollmera
"""

import os

def send2cloud_win():
    folder="C:\\KBApps\\AzCopy\\"
    folder="C:\\Users\\vollmera\\Documents\\SVN_home\\trunk\\SW_app\\github\\Rasp2Cloud\\"
    filename="2022_February_23_104650.csv"
    os.system('C:\\KBApps\\AzCopy\\azcopy copy "'+folder+filename+'" "https://testbenchpi4.blob.core.windows.net/achimpi4?sv=2020-08-04&st=2022-01-19T09%3A09%3A47Z&se=2023-09-20T08%3A09%3A00Z&sr=c&sp=racwdxlt&sig=o5eJidUhVuRDuIbUI%2BnaaACwAkEH4rFma4gBCsyjX7k%3D"')

    print('C:\\KBApps\\AzCopy\\azcopy copy '+folder+filename+'" "https://testbenchpi4.blob.core.windows.net/achimpi4?sv=2020-08-04&st=2022-01-19T09%3A09%3A47Z&se=2023-09-20T08%3A09%3A00Z&sr=c&sp=racwdxlt&sig=o5eJidUhVuRDuIbUI%2BnaaACwAkEH4rFma4gBCsyjX7k%3D"')
    
    
    
   
def send2cloud_rasp():
    dirList=os.listdir("/home/pi/EMBerry/log_data/")
    print(dirList)
    csvFile=[]
    for each in dirList:
            if ".csv" in each:
                    csvFile.append(each)
    print(csvFile)
    
    #sendString='sudo  blobxfer upload --storage-account testbenchpi4 --sas "?sv=2020-08-04&ss=bfqt&srt=co&sp=rwdlacupitfx&se=2022-01-30T17:03:10Z&st=2022-01-19T09:03:10Z&spr=https&sig=ykOpTDsq5TjWQ22ntcqrvgkhGg%2F2%2FUeb3qUbIen6MAg%3D" --remote-path achimpi4 --local-path /home/pi/Daq/files/'
    
    sendString= 'sudo blobxfer upload  --storage-account testbenchpi4 --sas "?sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2023-08-09T17:30:05Z&st=2022-02-10T10:30:05Z&spr=https&sig=%2BkcIcyTpUK0tHDiSBW4gC%2FvZP%2BrvSa5YS2neC7X%2BnfM%3D" --remote-path achimpi4 --local-path /home/pi/Daq/files/'
    
    for all in csvFile:
            print(all)
    
            os.system(sendString+str(all))
    

def send2cloud():    
    if os.name == 'nt':
        print("send for Windows")
        send2cloud_win()
    else:
        send2cloud_rasp()
        print("send for Rasp")
        
        
    
if __name__ == '__main__':
    # This will only be run when the module is called directly.
    send2cloud()