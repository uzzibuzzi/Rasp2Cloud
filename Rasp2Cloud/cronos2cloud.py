import ftplib
import os, sys
import shutil
from azure.storage.blob import BlockBlobService

### CONFIGURATION ###
cronos_ip = '192.168.100.133'
user = 'imc'
pw = 'imc'
azure_storage_account = 'dhpdataanalyticsstorage'
azure_sas_key = 'sv=2020-10-02&si=yanar-full&sr=c&sig=GSiSw9cNFFCy%2FWo1Cubs%2BqQLqecZQfqHcpby6or%2Fi5w%3D'
azure_path = 'yanar/pcmcia'
azure_blob_container = 'yanar'
# directory in Cronos to read from
cronos_dir = 'pcmcia' 
# directory in Raspberry to save the cronos files locally
raspberry_dir = '/home/pi/Cronos2Cloud' 
# filepath in Raspberry to read files from 
raspberry_read_path = raspberry_dir + '/pcmcia/'


def cronos_connect():
    """ establish the FTP connection to Cronos """
    try:
        ftp = ftplib.FTP(cronos_ip, user, pw)
        ftp.encoding = 'utf-8'
        print ("Connection to Cronos established!")
        return ftp
    except ftplib.error_perm as e:
        print("Connection to Cronos could not be established! Check IP, user and password.")

def pi_mkdir():
    """ create local directory in raspberry """
    if not os.path.isdir(raspberry_dir):
        oldmask = os.umask(000)
        os.makedirs(raspberry_dir,mode=0o777)
        os.umask(oldmask)

def send2cloud():
    """ send selected cronos files to cloud """
    os_command = 'blobxfer upload  --storage-account ' + azure_storage_account + ' --sas ' + azure_sas_key + ' --remote-path ' + azure_path + ' --local-path ' + raspberry_read_path
    os.system(os_command)

def get_cloud_content():
    """ get content of blob storage """
    block_blob_service = BlockBlobService(account_name=azure_storage_account, sas_token=azure_sas_key)
    return block_blob_service

def check_cloud_content(piContent):
    """ check if new files are added """
    block_blob_service = get_cloud_content()
    blobContent = block_blob_service.list_blobs(azure_blob_container)
    blobFiles = []
    for content in blobContent:
        content_name_raw = content.name
        if "pcmcia" in content_name_raw:
            content_name = content_name_raw.split('/', 4)[-2]
            blobFiles.append(content_name)
    blobFiles = list(dict.fromkeys(blobFiles))
    filesMissing = []
    for piFile in piContent:
        if piFile not in blobFiles:
            filesMissing.append(piFile)
        else:
            pass
    return filesMissing

def cronos2pi():
    pi_mkdir()
    ftp = cronos_connect()
    folders_cronos = ftp.nlst(cronos_dir)
    ftp.quit()
    for folder in folders_cronos:
        ftp = cronos_connect()
        print(folder)
        # destination_folder = destination_dir + '/' + cronos_dir + '/' + folder
        # pi_mkdir(destination_folder)
        # ftp.cwd(cronos_dir + '/' + folder)
        # files_in_folder = []
        # ftp.dir(files_in_folder.append)
        # for file in files_in_folder:
        #     filename = file.split(None, 8)[-1]
        #     if filename != 'DirClosed': #this is a random empty file
        #         # download the file
        #         local_filepath = os.path.join(destination_folder, filename)
        #         lf = open(local_filepath, "wb")
        #         ftp.retrbinary("RETR " + filename, lf.write)
        #         lf.close()
        # print("Raspi upload finished!")