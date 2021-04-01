'''
    Script to download fan sourced TBBT transcripts, required file is episode_links.json
'''
import os
import json
import requests
from lxml import html
from os import path
import argparse


# allTranscripts = {}


def get_episode_text(season, index, episodeInfo):
    ep, title, link = episodeInfo[season][index]
    try:
        page = requests.get(link)
        tree = html.fromstring(page.content)
        p_count = tree.find_class('entrytext')[0]
    except:
        raise Exception("Failed for {ep}, {season}".format(ep=ep,season=season))   

    return p_count.text_content(),ep



def download_transcripts_from_url(filename, save_path, force):
    
    if len(os.listdir(save_path)) == 202 or not force:
        print("transcripts are already downloaded.")

    else:
        try:
            with open(filename,"r") as file_:
                episode_info =  json.load(file_)
                file_.close()

            for season in episode_info:
                print(f"Downloading transcripts for the {season}")

                for idx in range(0,len(episode_info[season])):
                    transcript, episode = get_episode_text(season, idx, episode_info)
                    episode_id = f"{season}_{episode}.txt"

                    path = os.path.join(save_path, episode_id)

                    with open(path,"w",encoding="utf-8") as fh:
                        fh.write(transcript)
                        fh.close()

                    print("Downloaded the transcripts into raw_corpus directory")

                    # allTranscripts[ep_id] = transcript

            # #TODO: don't store all data into memory
            # #dump all data into single file
            # with open("corpus.json","w") as corpus_file:
            #     json.dump(allTranscripts, corpus_file, indent=4)
            #     corpus_file.close()
        
        except FileNotFoundError:
            print(f"Could not file {filename}")



def download(episodes, save_path, force):

    #if the save dir does not exists, create a new one
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    
    download_transcripts_from_url(episodes, save_path, force)

    print(f"Downloaded the transcripts to {save_path} directory")



# Main Function
def main():
    
    parser = argparse.ArgumentParser(description="Download the TBBT corpus")
    parser.add_argument('-i', "--inputFile" ,help="location of episode_links.json file", default="episode_links.json")
    parser.add_argument("-s", "--save", help="folder location to save the transcripts file", default="./raw_corpus")
    parser.add_argument("-f", "--force", help="forcefully download all files", action='store_true')

    args = parser.parse_args()

    download(args.inputFile, args.save, args.force)
    


# Entry point
if __name__ == "__main__":
    main()