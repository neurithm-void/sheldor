'''
    Script to read the raw downloaded data, and convert it into a single csv sheet, containing input and output(expected sentence).
'''
import os
import re
import argparse
import pandas as pd

SENTENCE_INSIDE_BRACKETS_PATTERN = re.compile(r"\([\w\s,.]*\)")


def write_dialogs_to_csv(lines, save_path):
    
    input_ = []
    in_speaker = []
    output = []
    out_speaker = []
    col_names = ['in_speaker', 'input', 'out_speaker', 'output']

    for idx, line in enumerate(lines):
        splitted_line = line.split(":")

        if len(splitted_line)==2:
            speaker, dialog = splitted_line
            speaker = SENTENCE_INSIDE_BRACKETS_PATTERN.sub("", speaker)

            if speaker.lower() == "sheldon":  
                #take the preceding dialog. 
                prev_line = lines[idx-1].split(":")

                if len(prev_line) == 2:
                    prev_speaker, pre_dialog = prev_line
                    prev_speaker = SENTENCE_INSIDE_BRACKETS_PATTERN.sub("", prev_speaker)

                    if prev_speaker.lower() != "sheldon":
                        pre_dialog = SENTENCE_INSIDE_BRACKETS_PATTERN.sub("", pre_dialog)
                        dialog = SENTENCE_INSIDE_BRACKETS_PATTERN.sub("", dialog)

                        input_.append(pre_dialog.strip())
                        in_speaker.append(prev_speaker.strip())
                        output.append(dialog.strip())
                        out_speaker.append(speaker.strip())

    #write file to the csv file.
    cache_df = pd.DataFrame({"in_speaker": in_speaker, "input": input_, "out_speaker":out_speaker, "output":output})  

    if not os.path.isfile(save_path):
        cache_df.to_csv(save_path, header=col_names, encoding='utf-8')
    else: # else it exists so append without writing the header
        cache_df.to_csv(save_path, mode='a', header=False, encoding='utf-8')



def process_data(data_path, save_path):
    transcripts = os.listdir(data_path)

    for file_count in range(len(transcripts)):
        with open(os.path.join(data_path, transcripts[file_count]), encoding="utf-8") as file_:
            lines = file_.readlines()
        
        write_dialogs_to_csv(lines, save_path)
        
        print(f"processing {transcripts[file_count]} is done")
        



# Main Function
def main():

    parser = argparse.ArgumentParser(description="process raw data to single csv")
    parser.add_argument('-c', "--corpus" ,help="location of all downloaded raw corpus", default=False)
    parser.add_argument("-s", "--save", help="folder location to save the processed csv file", default=False)

    args = parser.parse_args()

    #save dir
    if not args.save:
        save_path = "./processed_corpus/processed_data.csv"
    else:
        save_path = args.save

    #if the save dir does not exists, create a new one 
    #TODO: should work for linux and MacOS
    save_dir = "/".join(save_path.split("/")[:-1])
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    if not args.corpus:
        process_data("../transcripts_download/raw_corpus", save_path)
    else:
        process_data(args.corpus, save_path)


    print(f"Downloaded the transcripts to {save_path} directory")



# Entry point
if __name__ == "__main__":
    main()