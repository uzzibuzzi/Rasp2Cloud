import os, sys
from azure.storage.blob import BlockBlobService


# required functions for cloud upload
def send2cloud_missing(emb_path, cloud_path, fileName):
    """ send missing files to Azure cloud """
    sendString= 'blobxfer upload  --storage-account testbenchpi4 --sas "?sv=2020-08-04&ss=bfqt&srt=sco&sp=rwdlacupitfx&se=2023-08-09T17:30:05Z&st=2022-02-10T10:30:05Z&spr=https&sig=%2BkcIcyTpUK0tHDiSBW4gC%2FvZP%2BrvSa5YS2neC7X%2BnfM%3D" --remote-path ' + cloud_path + ' --local-path '
    os.system(sendString+emb_path+fileName)

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
        if 'motor_2022' in content_name_raw:
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
    # string to search for in the cloud
    search_string = 'motor_2022'    
    # copy files and send it to cloud
    print("Copy to Cloud starts.")
    EMB_data_path = '/media/pi/2E19-DF01/log/'
    cloud_path = 'achimpi4'
    piContent = os.listdir(EMB_data_path)
    if len(piContent) != 0:
        filesMissing = check_cloud_content(piContent)
        if len(filesMissing)!=0:
            for f in filesMissing:
                send2cloud_missing(EMB_data_path, cloud_path, f)
            print("Cloud upload finished.")
        else:
            print("No files missing")
    else:
        print("No files to send to cloud")