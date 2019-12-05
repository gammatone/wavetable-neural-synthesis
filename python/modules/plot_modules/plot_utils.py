#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-05 19:34:42
# @Author  : gammatone (adrien.bardet@live.fr)
# @Link    : https://github.com/gammatone/wavetable-neural-synthesis
# @Version : $Id$

"""
plot_utils.py
Module gathering useful plotting functions
"""

import matplotlib.pyplot as plt

def plot_1d(array_toplot, title=None):
    """
    Arguments
        array_toplot (np_array)
        title (str)
    """
    plt.plot(array_toplot)
    if title is not None:
        plt.title(title)
    plt.show()



