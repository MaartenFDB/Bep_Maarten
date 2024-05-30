import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import numpy as np

# Define example parameters
lowcut = 0.01  # Low cutoff frequency in Hz
highcut = 3  # High cutoff frequency in Hz
fs = 100.0  # Sampling frequency in Hz
order = 10  # Filter order

def butter_bandpass(lowcut, highcut, fs, order):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a


#def butter_bandpass_filter(Snelheid_abswaarde_vector, lowcut, highcut, fs, order):
   # b, a = butter_bandpass(lowcut, highcut, fs, order=order)
   # if np.isscalar(Snelheid_abswaarde_vector):
   #     Snelheid_abswaarde_vector = np.array([Snelheid_abswaarde_vector])
   # elif Snelheid_abswaarde_vector.ndim != 1:
   #     raise ValueError("Snelheid vector should be a 1-D array")
   # filtered_snelheid_abswaarde_vector = filtfilt(b, a, Snelheid_abswaarde_vector)
   # return filtered_snelheid_abswaarde_vector

def butter_bandpass_filter(Snelheid_abswaarde_vector, lowcut, highcut, fs, order):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    if np.isscalar(Snelheid_abswaarde_vector):
        Snelheid_abswaarde_vector = np.array([Snelheid_abswaarde_vector])
    elif Snelheid_abswaarde_vector.ndim != 1:
        raise ValueError("Snelheid vector should be a 1-D array")
    padlen = min(len(Snelheid_abswaarde_vector)-1, 3*(max(len(a),len(b)) - 1))
    filtered_snelheid_abswaarde_vector = filtfilt(b, a, Snelheid_abswaarde_vector, padlen=padlen)
    return filtered_snelheid_abswaarde_vector

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

#
##
#
############################################################################################


#Moving average filter:
def moving_average_filter(data, window_time, fs):
    window_size = int(window_time * fs)
    cumsum = np.cumsum(np.insert(data, 0, 0))
    filtered_data = (cumsum[window_size:] - cumsum[:-window_size]) / window_size
    return np.concatenate((data[:window_size-1], filtered_data))

fs = 1000.0  # Sampling frequency (Hz)
window_time = 0.1  # Window size for the moving average filter (seconds)

# Apply the moving average filter
filtered_data = moving_average_filter(data, window_time, fs)
# Apply the bandpass filter
#filtered_theta_dot = butter_bandpass_filter(theta_dot, lowcut, highcut, fs, order)

# Dit is om te plotten, maar Plot.py doet dat al.
# # Plot the original and filtered data
# plt.figure()
# plt.plot(t, theta_dot, label='Original theta_dot')
# plt.plot(t, filtered_theta_dot, label='Filtered theta_dot')
# plt.xlabel('Time [s]')
# plt.ylabel('Amplitude')
# plt.title('Butterworth Bandpass Filter (Order = 2)')
# plt.legend()
# plt.grid(True)
# plt.show()
