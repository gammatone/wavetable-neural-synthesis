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
    # check if exists, if not create it
    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)

    # Create a dataset manager
    my_dataset_manager = AKWF_Dataset(raw_data_dir)
    # clone git repo
    my_dataset_manager.clone_git_repo()


    return

if __name__ == "__main__":
    main()
