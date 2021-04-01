"""
function to setup environment based on selected experiment number. 
1. download all the dataa
"""

import os
import sys
import yaml
import argparse
from utils.download_files import download_req_files
from utils.transcripts_download import download_transcripts


DEFAULT_EXPERIMENT_YAML = "./experiments.yaml"
FILES_DOWNLOAD_PATH = "./downloads"
EPISODE_LINK_JSON = "./utils/transcripts_download/episode_links.json"


def main():

    parser = argparse.ArgumentParser(description="function to setup env based on selected experiment.")
    parser.add_argument('-e', "--experiment", help="experiment number, whose env needed is needed to be setup, default one", default="one")
    parser.add_argument('-c', "--config", help="experiments config file", default=DEFAULT_EXPERIMENT_YAML)
    parser.add_argument("-f", "--force", help="forcefully download all files", action='store_true')

    args = parser.parse_args()

    with open(args.config) as yaml_file:
        expriments = yaml.safe_load(yaml_file)

    experiment_details = expriments[f"experiment {args.experiment}"]
    files_download_path = experiment_details.get("files_download_path", FILES_DOWNLOAD_PATH)
    files_required = experiment_details["files_required"]

    download_req_files(files_required, files_download_path, args.force)
    download_transcripts.download(experiment_details.get("episode_links", EPISODE_LINK_JSON), f"{files_download_path}/raw_corpus", args.force)

    #TODO: Add other experiments requirements

if __name__ == "__main__":
    main()