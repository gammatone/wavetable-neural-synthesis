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

import numpy as np

# Append custom modules directory
sys.path.append('../modules/dataset_modules')
sys.path.append('../modules/dsp_modules')
sys.path.append('../modules/plot_modules')

# Custom import
from manage_AKWF_dataset import AKWF_Dataset

from plot_utils import plot_1d

def main():

    # define raw data directory
    raw_data_dir = "../data/raw_data"
    # define expected repo name
    repo_name = "AKWF-FREE"
    # define save dataset dir
    save_dataset_dir = "../data/datasets"
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

    print("=======================")
    print("WAV file analysis \t..."  )

    # Parse constain directory to look for .wav files
    print("\t-----------------------")
    print("\tParsing {} directory \t...".format(constrain_dir))
    wavfiles_nb, total_size, has_same_size = my_dataset_manager.wavfiles_analysis(constrain_dir)
    print("\t\tfiles number: {}".format(wavfiles_nb))
    print("\t\ttotal size: {} bytes".format(total_size))
    print("\t\tSame file size: {}".format(has_same_size))
    print("\tParsing {} directory \tDone".format(constrain_dir))

    # Check and load .wav files in a numpy array, only if they look like single-cycle waves
    print("\t-----------------------")
    print("\tChecking and loading'.wav' single-cycle waves files \t...")
    valid_scw_array = my_dataset_manager.check_load_scw_files()
    # # plot some arrays at some random index
    for i in range(10):
        randindex = np.random.randint(0, valid_scw_array.shape[0])
        plot_1d(valid_scw_array[randindex], title="Random sample across the single-cycle waves dataset")

    print("\tChecking and loading'.wav' single-cycle waves files \tDone")

    print("\t-----------------------")
    print("\tSaving single-cycle waves dataset in .npy file \t...")
    # check if directory exists, if not create it
    if not os.path.exists(save_dataset_dir):
        os.makedirs(save_dataset_dir)
    # define name of dataset
    dataset_filename = "dataset_{}_{}.npy".format(  
                                                    os.path.basename(os.path.normpath(my_dataset_manager.constrain_absdir)),
                                                    valid_scw_array.shape[0]
                                                    )
    np.save(os.path.join(save_dataset_dir, dataset_filename), valid_scw_array)

    print("\tSaving single-cycle waves dataset in .npy file \tDone")
    print("\tDataset saved in {} file.".format(os.path.join(save_dataset_dir, dataset_filename)))

    print("WAV file analysis \tDone"  )



    return

if __name__ == "__main__":
    main()
