import matplotlib.pyplot as plt
import numpy as np

def plot_color_text(filtered,predicted_beats,start_stop):
    minimum = min(filtered)
    maximum = max(filtered)
    lel = [np.arange(data[0],data[1]) for data in start_stop]
    #plt.plot(ecg_raw)
    plt.plot(filtered)
    for i in range(len(predicted_beats)):
        if (predicted_beats[i] != "N"):
            plt.fill_between(lel[i],minimum,maximum,facecolor='red', alpha=0.5)
            plt.text(start_stop[i][0],maximum,predicted_beats[i])
    #plt.scatter(peaks, [filtered[peaks[i]] for i in range(len(peaks))],c='red')
    plt.show()
def plot_with_rpeaks(filtered,r_peaks):
    peaks = [filtered[peak] for peak in r_peaks]
    plt.plot(filtered)
    plt.scatter(r_peaks,peaks,c='red')