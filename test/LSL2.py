"""Example program to show how to read a multi-channel time series from LSL."""
import time
from pylsl import StreamInlet, resolve_stream
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from collections import deque
import pysiology


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
                print(sample)
                raw_pulse_signal.append(sample[0])
    newdata = pysiology.electromyography.butter_lowpass_filter(raw_pulse_signal, 0.1, 200, 5)
    print(newdata)
    print(raw_pulse_signal)
    print( "Avg Sampling Rate == {}".format(len(raw_pulse_signal) / duration) )
    plt.plot(raw_pulse_signal)
    plt.plot(newdata)
    plt.ylabel('raw analog signal')
    plt.show()

testLSLPulseData()