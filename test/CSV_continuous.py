import csv
import random
import time
from pylsl import StreamInlet, resolve_stream
from time import sleep
import numpy

duration = int(input("How long? "))

# first resolve an EEG stream on the lab network
print("looking for an EMG stream...")
streams = resolve_stream('type', 'EMG')

# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

sleep(0)

print("gathering data to plot...")

def LSL():


    start = time.time()

    raw_pulse_signal = []
    while True:
        chunk, timestamp = inlet.pull_chunk()
        if timestamp:
            for sample in chunk:
                #print(sample)
                raw_pulse_signal.append(sample[2])

    #print("Avg Sampling Rate == {}".format(len(raw_pulse_signal) / duration))
    #print(raw_pulse_signal)

    return sample[2]






def CSV():
    x_value = 0
    total_1 = 0


    fieldnames = ["x_value", "total_1"]


    with open('data.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    while True:

        with open('data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {
                "x_value": x_value,
                "total_1": total_1,
            }

            csv_writer.writerow(info)
            print(x_value, total_1)

            x_value += 1
            total_1 = LSL()


        time.sleep(0.005)