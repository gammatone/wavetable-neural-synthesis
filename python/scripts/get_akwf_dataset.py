#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-25 20:46:08
# @Author  : gammatone (adrien.bardet@live.fr)
# @Link    : https://github.com/gammatone/wavetable-neural-synthesis
# @Version : $Id$

"""
get_akwf_dataset.py
"""

import os
import sys
# Append custom modules directory
sys.path.append('../modules/dataset_modules')

# Custom import
from manage_AKWF_dataset import AKWF_Dataset

def main():

    # define raw data directory
    raw_data_dir = "../data/raw_data"
    # define expected repo name
    repo_name = "AKWF-FREE"
    # define akwf root folder
    akwf_root_dir = os.path.join(raw_data_dir, repo_name)
    # define constrain sub directory where to constrain raw data analysis

    # check if exists, if not create it
    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)

    # Create a dataset manager
    my_dataset_manager = AKWF_Dataset(repo_name, raw_data_dir)

    # check if repo already exists, if not clone repo
    if not os.path.exists(akwf_root_dir):
        # clone git repo
        my_dataset_manager.clone_git_repo()

    # For now constrain dataset only to files inside "AKWF-FREE/AKWF/" directory and subdirectories
    constrain_dir = os.path.join(akwf_root_dir, "AKWF")

    print("-------------------")
    print("WAV file analysis \t..."  )
    # Analyze .wav files in constrain_dir
    wavfiles_nb, total_size, has_same_size = my_dataset_manager.wavfiles_analysis(constrain_dir)
    print("files number: {}".format(wavfiles_nb))
    print("total size: {} bytes".format(total_size))
    print("Same file size: {}".format(has_same_size))

    print("WAV file analysis \tDone"  )


    return

if __name__ == "__main__":
    main()
