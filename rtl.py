from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt

sdr = RtlSdr()
sdr.sample_rate = 2.048e6 # Hz
sdr.center_freq = 100e6 # Hz
sdr.freq_correction = 60 # PPM
sdr.gain = 'auto'

samples = sdr.read_samples(256*1024)
sdr.close()

plt.specgram(samples, NFFT=1024, Fs=sdr.sample_rate, Fc=sdr.center_freq)
plt.show()