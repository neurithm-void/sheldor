import sys
import requests
import traceback
from tqdm import tqdm



def download_file(url, save_location, large_file = True):

    try:
        res = requests.get(url, stream = True)

        total_size_in_bytes = int(res.headers.get('content-length', 0))
        chunk_size = 1024 #1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        with open(save_location, "wb") as file_:
            for chunk in res.iter_content(chunk_size= chunk_size):
                progress_bar.update(len(chunk))
                file_.write(chunk)

        progress_bar.close()
    
    except:
        traceback.print_exc()

