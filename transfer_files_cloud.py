# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 12:05:21 2022

@author: vollmera
"""

import os
import csv
import pandas as pd


def writeLogfile(sendedFiles):
    """gets an list and add ist to an existing log file.
    if file doestn exist it creats ist"""
    folder="C:\\Users\\vollmera\\Documents\\SVN_home\\trunk\\SW_app\\github\\Rasp2Cloud\\log_data\\"
    transferlogfile=folder+"alreadySended.txt"
    
    try:
        mdf=pd.read_csv(transferlogfile)     
        alreadySended=list(mdf["sended"])
        for each in sendedFiles:
            alreadySended.append(each)
        print("schon sended:",alreadySended)
        print("to send",sendedFiles)
        df = pd.DataFrame (alreadySended, columns = ['sended'])
    except:
        df = pd.DataFrame (sendedFiles, columns = ['sended'])
    df.to_csv(transferlogfile)
        


def makeFileList(path):
    """this makes a list of files from path 
    all .csv files will be collected and compared with 
    the already sended files listed in the .txt file in path"""
    
    dirs=os.listdir(path)
    messfiles=[]
    for names in dirs:
        if names.endswith(".csv"):
            
            messfiles.append(names)
        if names.endswith(".txt"):
            logfilename=names
            print(logfilename)
        
    try:     #compare with already sended files out of file list
        transferlogfile=path+"alreadySended.txt"
        mdf=pd.read_csv(transferlogfile)
        alreadySended=list(mdf["sended"])
    except:
        alreadySended=[]
        alreadySended=[] # file doesnt exist start with empty compaison
    filToSend=set(messfiles)-set(alreadySended)
    return list(filToSend)

    
logfilename="alreadySended.txt"


def fileIsCLosed():
    import psutil    
    
    
    for proc in psutil.process_iter():
        try:
            # this returns the list of opened files by the current process
            flist = proc.open_files()
            if flist:
                print(proc.pid,proc.name)
                
                
                for nt in flist:
                    print("\t",nt.path)
                    
                
    try:
        open(logfilename) # or "a+", whatever you need
    except IOError:
        print("Could not open file! Please close Excel!")
    
    try:
        with open(logfilename, "r") as file:
            # Print the success message
            print("File has opened for reading.")
# Raise error if the file is opened before
    except IOError:
        print("File has opened already.")
    
    
    
    
    
    try:
        f = open(logfilename)
        print("file is closed")
    except:
        print("file is open")
    f.close()
    
    
    if f.closed:
        print ('file is closed')
    else:
        print("file is open")


            


def send2cloud_win():
    folder="C:\\KBApps\\AzCopy\\"
    folder="C:\\Users\\vollmera\\Documents\\SVN_home\\trunk\\SW_app\\github\\Rasp2Cloud\\log_data\\"
    messfiles=makeFileList(folder)                 
    
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