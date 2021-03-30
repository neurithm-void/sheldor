'''
    Script to download glove embeddings, unzip it and only keep required embedding file while deleting other
'''
from download import download_file
from utils import create_folder, extract_zip



def download_and_extract_glove():

    url = "http://nlp.stanford.edu/data/glove.6B.zip"
    save_path = "./downloads/glove.6B.zip"

    #if the save dir does not exists, create a new one 
    #TODO: should work for linux and MacOS
    save_dir = "/".join(save_path.split("/")[:-1])
    # if not os.path.exists(save_dir):
    #     os.mkdir(save_dir)       
    create_folder(save_dir)    
    download_file(url, save_path)

    #extract zip 
    extracted_path = "./downloads/"
    extract_zip(save_path, extract_zip)




if __name__ == "__main__":
    download_and_extract_glove()

