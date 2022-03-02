# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 12:05:21 2022

@author: vollmera
"""

import os
import csv
import pandas as pd


def writeLogfile(sendedFiles):
    folder="C:\\Users\\vollmera\\Documents\\SVN_home\\trunk\\SW_app\\github\\Rasp2Cloud\\log_data\\"
    transferlogfile=folder+"alreadySended.txt"
    df = pd.DataFrame (sendedFiles, columns = ['sended'])
    try:
        mdf=pd.read_csv(transferlogfile)     
        mdf=pd.concat([mdf, df])
        mdf.to_csv(transferlogfile)
    except:
        df.to_csv(transferlogfile)
        


def makeFileList(path):
    dirs=os.listdir(path)
    messfiles=[]
    for names in dirs:
        if names.endswith(".csv"):
            messfiles.append(names)
    try: 
        transferlogfile=path+"alreadySended.txt"
        mdf=pd.read_csv(transferlogfile)
        alreadySended=list(mdf["sended"])[:4]
    except:
        alreadySended=[]
        set(messfiles)-set(alreadySended)
    return set(messfiles)-alreadySended    
        



def send2cloud_win():
    folder="C:\\KBApps\\AzCopy\\"
    folder="C:\\Users\\vollmera\\Documents\\SVN_home\\trunk\\SW_app\\github\\Rasp2Cloud\\log_data\\"
    messfiles=makeFileList(folder)                 
    
    messfiles=messfiles[:5]
    
    
    for everyfile in messfiles:
        filename=everyfile
        print("sending .... ",everyfile)        
        #filename="2022_February_23_104650.csv"
        os.system('C:\\KBApps\\AzCopy\\azcopy copy "'+folder+filename+'" "https://testbenchpi4.blob.core.windows.net/achimpi4?sv=2020-08-04&st=2022-01-19T09%3A09%3A47Z&se=2023-09-20T08%3A09%3A00Z&sr=c&sp=racwdxlt&sig=o5eJidUhVuRDuIbUI%2BnaaACwAkEH4rFma4gBCsyjX7k%3D"')
    writeLogfile(messfiles)
    #    print('C:\\KBApps\\AzCopy\\azcopy copy '+folder+filename+'" "https://testbenchpi4.blob.core.windows.net/achimpi4?sv=2020-08-04&st=2022-01-19T09%3A09%3A47Z&se=2023-09-20T08%3A09%3A00Z&sr=c&sp=racwdxlt&sig=o5eJidUhVuRDuIbUI%2BnaaACwAkEH4rFma4gBCsyjX7k%3D"')
    
    
    
   
def send2cloud_rasp():
    
    sendString= 'blobxfer upload  --storage-account testbenchpi4 --sas "?sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2023-08-09T17:30:05Z&st=2022-02-10T10:30:05Z&spr=https&sig=%2BkcIcyTpUK0tHDiSBW4gC%2FvZP%2BrvSa5YS2neC7X%2BnfM%3D" --remote-path achimpi4 --local-path '#'/home/pi/Daq/files/'
    
    folder="/home/pi/github/log_data/"
    messfiles=makeFileList(folder)                 
    print(messfiles)
    for everyfile  in messfiles:
        os.system(sendString+str(folder)+str(everyfile))
    writeLogfile(messfiles)
    
    

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