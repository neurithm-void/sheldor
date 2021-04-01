'''
    Script to download glove embeddings, unzip it and only keep required embedding file while deleting other
'''
import os
from .download import download_file
from .utils import create_folder, extract_zip



def download_and_extract_glove(save_dir, force):

    url = "http://nlp.stanford.edu/data/glove.6B.zip"
    save_path = f"{save_dir}/glove.6B.zip"
    extracted_path = f"{save_dir}/glove.6B" 


    if not os.path.exists(save_path) or force:
        #if the save dir does not exists, create a new one 
        create_folder(save_dir)    
        download_file(url, save_path)

        #extract zip
        print(f"extracting {save_path} ...")
        extract_zip(save_path, extracted_path)

        #delete downloaded zip file. 
        # os.remove(save_path)
    
    else:
        print(f"file glove.6B.zip already existed in {save_dir}")
        
        #TODO: update condit
        if not os.path.exists(f"{save_dir}/glove.6B"):
            print(f"extracting {save_path} ...")
            extract_zip(save_path, extracted_path)
        else:
            print(f"glove.6B folder already existed.")
                




if __name__ == "__main__":
    download_and_extract_glove()

