#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-12-04 19:05:57
# @Author  : gammatone (adrien.bardet@live.fr)
# @Link    : https://github.com/gammatone/wavetable-neural-synthesis
# @Version : $Id$

"""
dsp_utils.py
Module gathering useful DSP functions for audio analysis and processings
"""

import numpy as np
import librosa
from scipy.signal import find_peaks

from plot_utils import plot_1d

def librosa_load_wav(filepath):
    """
    Load wav file (using librosa) into numpy array

    Returns
        raw_array (np_array)
        sr (int):               samplerate value    
    """
    return librosa.load(filepath)

def normalize_1d(in_array, normal_method):
    """
    Arguments
        in_array (np array):        input array
        normal_method (str):        normalization method

    Returns
        norm_array (np array):      normalized array
    """
    if normal_method == "Peak":
        norm_array = in_array / np.max(np.abs(in_array))
    else:
        raise Exception("{} normalization method not implemented")

    return norm_array


def check_mono(np_array):
    return True if (len(np_array.shape) < 2 and len(np_array.shape) > 0) else False

def resample_from_length(in_array, resample_len, resample_method):
    """
    Resample the input array to fit it to the wanted resample_len length
    It uses librosa's resample() function which requires an original sr and a target sr
    So need to artificially estimate from these 2 the in_array length and the resample_len

    Arguments
        in_array (np array):        input array
        resample_len (int):         the length of the resampled array wanted
        resample_method (str):      method used to resample array

    Returns
        resample_array (np array):  resampled array
    """
    # artificially set an original samplerate
    or_sr = 22050
    # deduce a target samplerate
    target_sr = int(resample_len * or_sr / in_array.shape[0])
    # resample
    resample_array = librosa.resample(in_array, or_sr, target_sr, res_type=resample_method)
    # Now check array length and correct if does not correspond to resample_len
    if resample_array.shape[0] > resample_len:
        resample_array = resample_array[resample_len]
    elif resample_array.shape[0] < resample_len:
        resample_array = np.pad(resample_array, (0, resample_len - resample_array.shape[0]),
                                'constant', constant_values=(0, resample_array[0]))
    return resample_array



def check_load_scw(in_array, amp_thd, normal_method="Peak", resample_len=1024, resample_method="kaiser_best"):
    """
    Check input array single-cycle wave sanity, i.e. if it looks like single-cycle waves (scw)
    Process/normalize the array (length and amplitude)
    Return the array
    More precisely:
        - Check input array shape (should be mono)
        - Center array if offset
        - Check if amplitude max peak is not too low (if the case then exclude the file)
        - Check if first and last audio samples are equals (if not the case then exclude the file)
        - Check auto-correlation to be sure the file contains only 1 period of the signal 
        - normalize signal (according to Peak to Peak amp or RMS)
        - resample the array according to resample_len
        - return array

    Arguments
        in_array (np array):        input array
        amp_thd (float):            the amplitude threshold to be elligible as a scw
        normal_method (str):        normalization method
        resample_len (int):         common length (i.e. audio samples) of resampled arrays
        resample_method (str):      method used when resampling arrays

    Returns
        processed_array (np_array): if scw eligible
        else None 
    """
    processed_array = in_array[:]
    # Check mono shape
    if not check_mono(processed_array):
        return
    # Center array
    processed_array = processed_array - np.mean(processed_array)
    # Check amplitudes
    if np.max(np.abs(processed_array)) < amp_thd:
        return
    
    # Check first and last audio samples
    first_sample = processed_array[0]
    last_sample = processed_array[processed_array.shape[0]-1]
    abs_diff = np.abs(first_sample - last_sample)
    # define error margin
    err_margin = 1e-2
    if abs_diff < err_margin:
        return

    # Check auto-correlation using librosa
    autocorr_array = librosa.autocorrelate(processed_array)
    # find peaks in autocorr using scipy
    peaks_indexes, peaks_values = find_peaks(autocorr_array, height=0)
    # retrieve the 2nd max peak value (apart from the 0 index)
    if peaks_values["peak_heights"].shape[0] > 0:
        max_peak_val = np.max(peaks_values["peak_heights"])
        max_peak_index = peaks_indexes[np.argmax(peaks_values["peak_heights"])]
    else:
        max_peak_val = 0
        max_peak_index = 0
    # Considering that if the 2nd max value is above 0.9 * 1st peak value, the wave is not valid
    if max_peak_val > 0.8 * autocorr_array[0] and max_peak_index > int(processed_array.shape[0] / 10): 
        # plot_1d(processed_array)
        # plot_1d(autocorr_array)
        return

    # normalize
    processed_array = normalize_1d(processed_array, normal_method)
    # resample according to wanted wave length
    processed_array = resample_from_length(processed_array, resample_len, resample_method)

    return processed_array