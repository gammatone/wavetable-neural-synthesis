#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-03 20:47:13
# @Author  : gammatone (adrien.bardet@live.fr)
# @Link    : https://github.com/gammatone/wavetable-neural-synthesis
# @Version : $Id$

"""
manage_dataset.py
A set of classes to manage multi-format datasets
"""

import os
import sys

import numpy as np

# Custom import
from dsp_utils import librosa_load_wav, check_load_scw

class DatasetFromGit():
    """
    A class to manage datasets from a given repository
    Basically clone the repo in a target directory

    Attributes
        git_url (str):          url to the git repository
        repo_name (str):        repository name i.e. the root folder name of the repository
        save_dir (str):         path to directory where to localy save repository
        constrain_absdir(str):  directory where to perform analysis and processings on wav files
    """
    def __init__(self, git_url, repo_name, save_dir):
        self.git_url = git_url
        self.repo_name = repo_name
        self.save_dir = save_dir
        self.constrain_absdir = None

    def clone_git_repo(self):
        """ Clone repository following git_url into save_dir directory """
        clone_cmd = "git clone " + self.git_url

        os.chdir(os.path.abspath(self.save_dir))
        os.system(clone_cmd)

    def wavfiles_analysis(self, constrain_dir):
        """
        In constrain_dir and its subdirectories,
        count .wav files and total size in bytes,
        also check if their sample size differ or not

        Arguments
            constrain_dir (str):    the directory where to perform the analysis

        Returns
            wavfiles_nb (int):      number of .wav files parsed
            total_size (int):       total .wav files size in byte
            has_same_size (bool):   True if all files have same size else False
        """
        # First check if constrain_dir is a sub directory of repo_name
        repo_root_absdir = os.path.abspath(os.path.join(self.save_dir, self.repo_name))
        # Update constrain_absdir
        self.constrain_absdir = os.path.abspath(constrain_dir)
        if repo_root_absdir not in self.constrain_absdir:
            raise Exception("Trying to analyze a directory outside {} repository".format(repo_root_absdir))

        wavfiles_nb = 0
        total_size = 0
        has_same_size = True
        tmp_size = 0

        # Parse .wav files
        for root, subdirs, files in os.walk(self.constrain_absdir):
            for file in files:
                if file.endswith('.wav'):
                    wavfiles_nb += 1
                    new_size = os.path.getsize(os.path.join(root,file))
                    total_size += new_size
                    if wavfiles_nb == 1:
                        tmp_size = new_size
                    if new_size != tmp_size:
                        has_same_size = False

        return wavfiles_nb, total_size, has_same_size

    def check_load_scw_files(self):
        """
        Load .wav files in constrain directory and make sure they look like single-cycle waves
        Analyze and process them:
            - Center array if offset
            - Check if amplitude max peak is not too low (if the case then exclude the file)
            - Check if first and last audio samples are equals (if not the case then exclude the file)
            - Check auto-correlation to be sure the file contains only 1 period of the signal 
            - normalize signal (according to Peak to Peak amp or RMS)
            - resample the array according to array_len
            - append in numpy array
        If success store them in numpy array

        Returns
        scw_array (np array):   array of shape (scw nb, resample length) gathering all scw found 

        """
        # define dsp analysis and processings parameters
        amp_thd = 0.5
        normal_method = "Peak"
        resample_len = 1024
        resample_method = "kaiser_best"
        # define list of numpy array that will contain processed scw
        scw_list = []

        # Parse .wav files
        for root, subdirs, files in os.walk(self.constrain_absdir):
            for file in files:
                if file.endswith('.wav'):
                    # load wav file (using librosa) into numpy array
                    raw_array, sr =librosa_load_wav(os.path.join(root,file))
                    processed_array = check_load_scw(raw_array, amp_thd, normal_method, resample_len, resample_method)
                    if processed_array is not None:
                        scw_list.append(processed_array)


        scw_array = np.asarray(scw_list)
        print(scw_array.shape)

        return scw_array





