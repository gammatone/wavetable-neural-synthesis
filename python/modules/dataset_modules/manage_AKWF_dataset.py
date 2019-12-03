#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-03 20:39:07
# @Author  : gammatone (adrien.bardet@live.fr)
# @Link    : https://github.com/gammatone/wavetable-neural-synthesis
# @Version : $Id$

"""
manage_AKWF_dataset.py
Dataset handling from 'Adventure Kid Waveforms' repository: https://github.com/KristofferKarlAxelEkstrand/AKWF-FREE
A collection of one cycle waveforms to be used within synthesizers or other kinds of sound generators.
"""

# Custom import
from manage_dataset import DatasetFromGit

class AKWF_Dataset(DatasetFromGit):
    """
    A 'DatasetFromGit' child class to manage AKWF dataset

    Attributes
    """
    def __init__(self, repo_name, save_dir):
        git_url = "https://github.com/KristofferKarlAxelEkstrand/AKWF-FREE.git"
        super(AKWF_Dataset, self).__init__(git_url, repo_name, save_dir)


        