# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:31:47 2022

@author: vollmera
"""
import logging
import threading
import time
from fakeDaqRec import mainRecord

import os

def thread_function(name):
    logging.info("Thread %s: starting", name)
    
    folder="C:\\KBApps\\AzCopy\\"
    folder="C:\\Users\\vollmera\\Documents\\SVN_home\\trunk\\SW_app\\github\\Rasp2Cloud\\"
    filename="2022_February_23_104650.csv"
    os.system('C:\\KBApps\\AzCopy\\azcopy copy "'+folder+filename+'" "https://testbenchpi4.blob.core.windows.net/achimpi4?sv=2020-08-04&st=2022-01-19T09%3A09%3A47Z&se=2023-09-20T08%3A09%3A00Z&sr=c&sp=racwdxlt&sig=o5eJidUhVuRDuIbUI%2BnaaACwAkEH4rFma4gBCsyjX7k%3D"')
    
    
    print('C:\\KBApps\\AzCopy\\azcopy copy '+folder+filename+'" "https://testbenchpi4.blob.core.windows.net/achimpi4?sv=2020-08-04&st=2022-01-19T09%3A09%3A47Z&se=2023-09-20T08%3A09%3A00Z&sr=c&sp=racwdxlt&sig=o5eJidUhVuRDuIbUI%2BnaaACwAkEH4rFma4gBCsyjX7k%3D"')
    
    time.sleep(10)
    logging.info("Thread %s: finishing", name)




if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    while mainRecord():
        pass
        
    logging.info("Main    : all done")