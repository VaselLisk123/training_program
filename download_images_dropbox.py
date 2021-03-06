from email.mime import image
import requests
import zipfile
import os
from PIL import Image
import glob

def creating_file(row):
    if os.path.exists(f"D:\\Piton\\training_program\\downloaded_images\\{row['Name'],row['Barcode']}"):
        pass
    else:
        extract_path = os.mkdir(f"D:\\Piton\\training_program\\downloaded_images\\{row['Name'],row['Barcode']}")
        new_path = f"D:\\Piton\\training_program\\downloaded_images\\{row['Name'],row['Barcode']}"
    return new_path

def modifying_dropbox_url(link):
    cuted_url = link[:-1]
    new_url = cuted_url + "1"
    return new_url

def download_file_dropbox(row):
    downloaded_file = requests.get(modifying_dropbox_url(str(row["Asset Link"])))
    zip_path = f"D:\\Piton\\training_program\\downloaded_images\\{row['Name'],row['Barcode']}.zip"
    if os.path.exists(zip_path):
        pass
    else:
        dest_file = open(zip_path,"wb")
        dest_file.write(downloaded_file.content)
        unarchiving_zip_file(zip_path,row)

def unarchiving_zip_file(file_destination,row):
    with zipfile.ZipFile(file_destination,"r") as zip_ref:
        zip_ref.extractall(creating_file(row))

def get_images(row):
    image_list = []
    for filename in glob.glob(f"D:\\Piton\\training_program\\downloaded_images\\{row['Name'],row['Barcode']}\\*.png"):
        image_list.append(filename)
    for filename in glob.glob(f"D:\\Piton\\training_program\\downloaded_images\\{row['Name'],row['Barcode']}\\*.jpg"):
        image_list.append(filename)
    return image_list
