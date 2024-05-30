import numpy as np
from scipy.signal import butter, filtfilt

def butter_lowpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    
    # Ensure input data array has sufficient length for filtering
    if len(data) < 3 * max(len(a), len(b)):
        raise ValueError("Input data array is too short for filtering. Add more data points.")
    
    y = filtfilt(b, a, data)
    return y
