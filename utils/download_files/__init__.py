# if __name__ == "__main__":

#     import argparse
#     from download_glove import download_and_extract_glove;

#     parser = argparse.ArgumentParser(description="download required files specified by the user, if none selected code will download all")
#     parser.add_argument('-d', "--downloads", nargs="+", help="name of the files needed to download", default=["glove"])
#     parser.add_argument("-s", "--save", help="folder location to save downloaded files", default="./downloads")
#     parser.add_argument("-f", "--force", help="forcefully download all files", action='store_true')

#     args = parser.parse_args()

#     download_req_files(args.downloads, args.save, args.force)    


# else:
from .download_glove import download_and_extract_glove



def download_req_files(files, save_path, force):

    if "glove" in files:
        download_and_extract_glove(save_path, force)
    
    else:
        print("no files to download.")
        
