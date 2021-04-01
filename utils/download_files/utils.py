'''
    Collection of all utils 
'''
import os
import zipfile


def extract_zip(zip_path, extracted_path):

    with zipfile.ZipFile(zip_path,"r") as zip_ref:
        zip_ref.extractall(extracted_path)


def create_folder(save_dir):

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)          


