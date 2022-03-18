# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:31:47 2022

@author: vollmera
"""

import threading
import time

from transfer_files_cloud import send2cloud
from thread_scan import continuesrecord

def thread_function(name):

    send2cloud()
    time.sleep(100)




if __name__ == "__main__":
    x = threading.Thread(target=thread_function, args=(1,))

    x.start()
    # x.join()
    while continuesrecord():
        pass
    
 