import os, sys
import shutil
import time
import datetime
from azure.storage.blob import BlockBlobService
import pandas as pd

    
def send2cloud_all(daqhats_path, cloud_path):
    """ send files to Azure cloud """
    sendString= 'blobxfer upload  --storage-account testbenchpi4 --sas "?sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2023-08-09T17:30:05Z&st=2022-02-10T10:30:05Z&spr=https&sig=%2BkcIcyTpUK0tHDiSBW4gC%2FvZP%2BrvSa5YS2neC7X%2BnfM%3D" --remote-path ' + cloud_path + ' --local-path '
    os.system(sendString+daqhats_path)

def send2cloud_missing(daqhats_path, cloud_path, fileName):
    """ send missing files to Azure cloud """
    sendString= 'blobxfer upload  --storage-account testbenchpi4 --sas "?sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2023-08-09T17:30:05Z&st=2022-02-10T10:30:05Z&spr=https&sig=%2BkcIcyTpUK0tHDiSBW4gC%2FvZP%2BrvSa5YS2neC7X%2BnfM%3D" --remote-path ' + cloud_path + ' --local-path '
    os.system(sendString+daqhats_path+fileName)

def get_cloud_content():
    """ get content of blob storage """
    account_name = 'testbenchpi4'
    sas_token = "?sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2023-08-09T17:30:05Z&st=2022-02-10T10:30:05Z&spr=https&sig=%2BkcIcyTpUK0tHDiSBW4gC%2FvZP%2BrvSa5YS2neC7X%2BnfM%3D"
    blob_container = 'achimpi4'
    block_blob_service = BlockBlobService(account_name=account_name, sas_token=sas_token)
    return block_blob_service, blob_container
   
def check_cloud_content(piContent):
    # compare Cronos data with cloud
    block_blob_service, blob_container = get_cloud_content()
    blobContent = block_blob_service.list_blobs(blob_container)
    blobFiles = []
    for content in blobContent:
        content_name_raw = content.name
        if 'DevAddr' in content_name_raw:
            content_name = content_name_raw.split('/', 7)[-1]
            blobFiles.append(content_name)
    blobFiles = list(dict.fromkeys(blobFiles))
    filesMissing = []
    for piFile in piContent:
        if piFile not in blobFiles:
            filesMissing.append(piFile)
        else:
            pass
    return filesMissing



if __name__ == '__main__':
    daqhats_path = '/home/pi/daqhats/examples/c/mcc118/three_boards/LogFiles/' 
    cloud_path = 'achimpi4/daqhats/examples/c/mcc118/three_boards/LogFiles'
    piContent = os.listdir(daqhats_path)
    #send2cloud_all(daqhats_path, cloud_path)
    filesMissing = check_cloud_content(piContent)
    if len(filesMissing)!=0:
        for f in filesMissing:
            df = pd.read_csv(daqhats_path+f)
            if df['Day Time'].values[-1]=='FINISHED':
                send2cloud_missing(daqhats_path, cloud_path, f)
    else:
        print("No files missing")