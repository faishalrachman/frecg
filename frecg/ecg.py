# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 23:06:14 2018

@author: Faishal Rachman
"""
from biosppy.signals import ecg, tools as st
import numpy as np
import pickle
from frecg.tools import *

def filter_ecg(signal=None,sampling_rate=1000.):
    order = int(0.3 * sampling_rate)
    filtered, _, _ = st.filter_signal(signal=signal,
                                  ftype='FIR',
                                  band='bandpass',
                                  order=order,
                                  frequency=[3, 45],
                                  sampling_rate=sampling_rate)
    return filtered

def classify_peaks(r_peaks, sampling_rate=250.):
#    classes = ["N" for i in range(len(r_peaks))]
    clf = pickle.load(open('../model_jadi/model_ann.sav','rb'))
    feature, max_rr, min_rr, rr_list, start_stop_feature = extract_RR(r_peaks,sampling_rate=sampling_rate)
    predicted_beats = clf.predict(feature)
    hr = get_hr(rr_list,sampling_rate)
    if (len(hr) == 0):
        hr = [0]
    return feature, predicted_beats, [max_rr, min_rr], [max(hr), min(hr)], start_stop_feature