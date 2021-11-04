from scipy.signal import kaiserord, lfilter, firwin, freqz

def LPF(signal, cutoff_hz, fs):
    nyq_rate = fs/2.0
    width = 5.0/nyq_rate
    ripple_db = 60.0
    N , beta = kaiserord(ripple_db, width)
    taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    filtered = lfilter(taps, 1.0, signal)
    return filtered
