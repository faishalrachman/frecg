# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 23:04:32 2018

@author: Faishal Rachman
"""

import pandas as pd
import numpy as np

def splitted_file_load(file):
    data = pd.read_csv(file)
    return data.iloc[:,1::].values

def mitbih_file_load(file):
    f = open(file, 'r')
    lines = f.readlines()
    lines.pop(0)
    f.close()
    ecg_data = []
    for hihi in lines:
        try:
            ecg_data.append(float(hihi.split(',')[1]))
        except ValueError:
            print (hihi)
    return ecg_data

def create_summary_minute(beat_class,rr,hr):
    beat_count = pd.Series(beat_class).value_counts()
    rr_max = rr[0]
    rr_min = rr[1]
    hr_max = hr[0]
    hr_min = hr[1]
    try:
        pvc_count = beat_count['V']
    except:
        pvc_count = 0
    try:
        pac_count = beat_count['A']
    except:
        pac_count = 0
    try:
        af_count = beat_count['F']
    except:
        af_count = 0
        
    try:
        normal_count = beat_count['N']
    except:
        normal_count = 0
                
        
    return [rr_max, rr_min, hr_max, hr_min, pvc_count, pac_count, af_count, normal_count]
def save_summary_tocsv(summary,filename):
    df = pd.DataFrame(summary, columns=["rr_max", "rr_min", "hr_max", "hr_min", "PVC", "PAC", "AF","Normal"])
    df.index += 1
    df.to_csv(filename)

def extract_RR(r_peaks, sampling_rate=250):

    rr_list = [[(r_peaks[i+1] - r_peaks[i]),[r_peaks[i], r_peaks[i+1]]] for i in range(0,len(r_peaks) - 1)]

    """
    Fitur yang digunakan adalah
    window 1
    window 2
    window 3
    window 4
    window 5
    """
#    feature = [[rr_list[i][0],rr_list[i+1][0],rr_list[i+2][0],rr_list[i+3][0],rr_list[i+4][0]] for i in range(len(rr_list) - 4)]
    feature = []
    start_stop_feature = []
    for i in range(len(rr_list) - 4):
        feature.append([rr_list[i][0],rr_list[i+1][0],rr_list[i+2][0],rr_list[i+3][0],rr_list[i+4][0]])
        start_stop_feature.append(rr_list[i+2][1])
    max_rr = max(rr_list, key=lambda x: x[0])[0]
    min_rr = min(rr_list, key=lambda x: x[0])[0]
    return feature, max_rr/sampling_rate, min_rr/sampling_rate, rr_list, start_stop_feature

def getr_peaks(arraynya):
    status = 0 #bawah 1 atas
    R = 0.7 * max(arraynya)
#    R = 0.2
    r_peaks = []
    datatemp = []
    temp = []
    for i in range(len(arraynya)):
        data = arraynya[i]
        if (data > R and status == 0):
            status = 1
        if (data > R and status == 1):
            datatemp.append(data)
            temp.append(i)
        if (data <= R and status == 1):
            indextertinggi = temp[datatemp.index(max(datatemp))]
            r_peaks.append(indextertinggi)
            datatemp = []
            temp = []
            status = 0
    return r_peaks

def get_hr(rr_list,sampling_rate=250):
    lel = []
    for i in range(len(rr_list)):
        lel.append(60/(rr_list[i][0]/sampling_rate))
    return lel