from frecg.tools import *
from frecg.ecg import *
from biosppy.signals.ecg import hamilton_segmenter, correct_rpeaks
import os


for root, dirs, files in os.walk("data_pasien/splitted/"):
    for file in files:
        dataset = splitted_file_load("data_pasien/splitted/%s" % file)
        summary = []
        for ecg_raw in dataset:
            filtered = filter_ecg(signal=ecg_raw,sampling_rate=250)
#            r_peaks = getr_peaks(filtered)    # segment
            rpeaks, = hamilton_segmenter(signal=filtered, sampling_rate=250)
            r_peaks, = correct_rpeaks(signal=filtered,
                                     rpeaks=rpeaks,
                                     sampling_rate=250,
                                     tol=0.05)
            if (len(r_peaks) > 5):
                feature, predicted_beats, rr, hr, start_stop = classify_peaks(r_peaks)
                summary.append(create_summary_minute(predicted_beats,rr,hr))
        print(file, "done")
        save_summary_tocsv(summary,'result/'+file)

        