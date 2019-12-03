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

class DatasetFromGit():
    """
    A class to manage datasets from a given repository
    Basically clone the repo in a target directory

    Attributes
        git_url (str):          url to the git repository
        save_dir (str):         path to directory where to localy save repository
    """
    def __init__(self, git_url, save_dir):
        self.git_url = git_url
        self.save_dir = save_dir

    def clone_git_repo(self):
        """ Clone repository following git_url into save_dir directory """
        clone_cmd = "git clone " + self.git_url

        os.chdir(os.path.abspath(self.save_dir))
        os.system(clone_cmd)

