### IMPORTS ###
import ftplib
import os, sys
import subprocess
import shutil
from azure.storage.blob import BlockBlobService
import time

### CONFIGURATION CRONOS & AZURE ACCOUNT ###
cronos_ip = '192.168.100.231'
user = 'imc'
pw = 'imc'
azure_storage_name = "testbenchpi4"
# IMPORTANT: sas_key needs to be typed manually into the "os_command" line in the function "send2cloud"
azure_sas_key = "?sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2023-08-09T17:30:05Z&st=2022-02-10T10:30:05Z&spr=https&sig=%2BkcIcyTpUK0tHDiSBW4gC%2FvZP%2BrvSa5YS2neC7X%2BnfM%3D"
azure_path = 'achimpi4/Cronos2Cloud'
azure_blob_container = 'achimpi4'
# directory in Cronos to read from
cronos_dir = 'pcmcia' 
# directory in Raspberry to save the cronos files locally
raspberry_dir = '/home/pi/Cronos2Cloud'


def cronos_connect(message):
    """ establish the FTP connection to Cronos """
    try:
        ftp = ftplib.FTP(cronos_ip, user, pw)
        ftp.encoding = 'utf-8'
        if message == True:
            print ("Connection to Cronos established!")
        return ftp
    except ftplib.error_perm as e:
        print("Connection to Cronos could not be established! Check IP, user and password.")

def pi_mkdir(directory):
    """ create local directory in raspberry """
    if not os.path.isdir(raspberry_dir + '/' + directory):
        oldmask = os.umask(000)
        os.makedirs(raspberry_dir + '/' + directory,mode=0o777)
        os.umask(oldmask)

def send2cloud(read_path, azure_final_path):
    """ send selected cronos files to cloud """
    os_command = 'blobxfer upload  --storage-account ' + azure_storage_name + ' --sas "?sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2023-08-09T17:30:05Z&st=2022-02-10T10:30:05Z&spr=https&sig=%2BkcIcyTpUK0tHDiSBW4gC%2FvZP%2BrvSa5YS2neC7X%2BnfM%3D" --remote-path ' + azure_final_path + ' --local-path ' + read_path
    os.system(os_command)

def get_cloud_content():
    """ get content in blob storage """
    block_blob_service = BlockBlobService(account_name=azure_storage_name, sas_token=azure_sas_key)
    return block_blob_service

def check_cloud_content(experiment, experiment_date):
    """ check if experiment and experiment_date are missing in cloud """
    block_blob_service = get_cloud_content()
    blobContent = block_blob_service.list_blobs(azure_blob_container)
    blobFiles = []
    for content in blobContent:
        searchString = 'Cronos2Cloud'
        if searchString in content.name:
            blobFiles.append(content.name)
    blobFiles = list(dict.fromkeys(blobFiles))
    missing = True
    for f in blobFiles:
        if (experiment in f) and (experiment_date in f):
            missing = False
            print("Experiment: " +experiment+", Date: " + experiment_date + " already in cloud.")
            break
    return missing        
            
def cronos2cloud():
    ftp = cronos_connect(True)
    folders_cronos = ftp.nlst(cronos_dir)
    folders_cronos = [name for name in folders_cronos if 'EMB' in name]
    ftp.quit()
    for experiment in folders_cronos:
        pi_mkdir(experiment)
        ftp = cronos_connect(False)
        ftp.cwd(cronos_dir + '/' + experiment)
        experiment_dates = ftp.nlst()[:-1]
        ftp.quit()
        for date_raw in experiment_dates:
            date_raw2 = date_raw.split(None, 8)[-1]
            date = date_raw2[:-4].replace(" ","_")
            if check_cloud_content(experiment, date) == True:
                pi_mkdir(experiment + '/' + date)
                ftp = cronos_connect(False)
                ftp.cwd(cronos_dir + '/' + experiment + '/' + date_raw2)
                experiment_files = ftp.nlst()
                for file_raw in experiment_files:
                    file = file_raw.split(None, 8)[-1]
                    if file != 'DirClosed':
                        local_filepath = os.path.join(raspberry_dir + '/' + experiment + '/' + date, file)
                        lf = open(local_filepath, "wb")
                        ftp.retrbinary("RETR " + file, lf.write)
                        lf.close()
                        send2cloud(raspberry_dir + '/' + experiment + '/' + date + '/' + file, azure_path + '/' + experiment + '/' + date)
                print("Experiment: "+experiment+", Date: "+date+", Cloud update done.")       
                ftp.quit()
            else:
                ftp = cronos_connect(False)
                ftp.cwd(cronos_dir + '/' + experiment + '/' + date_raw2)
                experiment_files = ftp.nlst()
                for file_raw in experiment_files:
                    file = file_raw.split(None, 8)[-1]
                    ftp.delete(file)
                ftp.quit()
                ftp = cronos_connect(False)
                ftp.cwd(cronos_dir + '/' + experiment)                
                ftp.rmd(date_raw2)
                print("Experiment: "+experiment+", Date: "+date+", deleted from Cronos.")       
                ftp.quit()
                

        
if __name__ == '__main__':
    while(1):
        print("Cronos query running...")
        cronos2cloud()
        print("Cronos query done. Waiting one hour to start new query.")
        time.sleep(3600)