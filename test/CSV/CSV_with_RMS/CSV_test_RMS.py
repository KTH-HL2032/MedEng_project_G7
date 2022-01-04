import csv
import random
import time
from time import sleep
import numpy
from pylsl import StreamInlet, resolve_stream
import math

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

x_value = 0
total_1 = 0


fieldnames = ["x_value", "total_1"]

# first resolve an EEG stream on the lab network
print("looking for an EMG stream...")
streams = resolve_stream('type', 'EMG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

sleep(0)

print("gathering data to plot...")


with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

raw_pulse_signal = []

while True:

    if True:
        chunk, timestamp = inlet.pull_chunk()

        if timestamp:
            for sample in chunk:
                raw_pulse_signal.append(sample[2])
                print(rms(raw_pulse_signal, 128))


                with open('data.csv', 'a') as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                    info = {
                        "x_value": x_value,
                        "total_1": total_1,
                    }

                    csv_writer.writerow(info)
                    print(x_value, total_1)

                    x_value += 1
                    total_1 = 1 # <---- sample values from EMG-signal have to come here


                    time.sleep(0.005)
