# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:31:47 2022

@author: vollmera
"""
import logging
import threading
import time
from fakeDaqRec import mainRecord
#from transfer_files_rasp import send2cloud
from transfer_files_cloud import send2cloud
from DRC import main

def thread_function(name):
    logging.info("Thread %s: starting", name)
    send2cloud()
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
        main()
        pass
        
    logging.info("Main    : all done")
    
    
 