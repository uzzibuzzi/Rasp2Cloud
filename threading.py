# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 09:31:47 2022

@author: vollmera
"""

import threading
import time
from fakeDaqRec import mainRecord

from transfer_files_cloud import send2cloud


def thread_function(name):

    send2cloud()
    time.sleep(10)




if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    x = threading.Thread(target=thread_function, args=(1,))

    x.start()
    # x.join()
    while mainRecord():
        pass
    
 