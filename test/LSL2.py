"""Example program to show how to read a multi-channel time series from LSL."""
import time
from pylsl import StreamInlet, resolve_stream
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from collections import deque
import pysiology
import numpy
import math


duration = int(input("How long? "))

# first resolve an EEG stream on the lab network
print("looking for an EMG stream...")
streams = resolve_stream('type', 'EMG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

sleep(0)

print("gathering data to plot...")

def testLSLPulseData():
    start = time.time()

    raw_pulse_signal = []
    while time.time() <= start + duration:
        chunk, timestamp = inlet.pull_chunk()
        if timestamp:
            for sample in chunk:
                print(sample[2])
                raw_pulse_signal.append(sample[2])

    print("Avg Sampling Rate == {}".format(len(raw_pulse_signal) / duration))
    print(raw_pulse_signal)


    def rms(interval, halfwindow):
        """ performs the moving-window smoothing of a signal using RMS """
        n = len(interval)
        rms_signal = numpy.zeros(n)
        for i in range(n):
            small_index = max(0, i - halfwindow)  # intended to avoid boundary effect
            big_index = min(n, i + halfwindow)  # intended to avoid boundary effect
            window_samples = interval[small_index:big_index]

            # here is the RMS of the window, being attributed to rms_signal 'i'th sample:
            rms_signal[i] = math.sqrt(sum([s ** 2 for s in window_samples]) / len(window_samples))

        return rms_signal

    print(rms(raw_pulse_signal, 2))

    threshold = 150

    # plt.plot(listdata)
    plt.plot(rms(raw_pulse_signal, 80))
    #plt.plot(threshold)

    plt.plot(raw_pulse_signal)
    plt.ylabel('raw analog signal')
    plt.show()

testLSLPulseData()