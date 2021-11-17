import csv
import random
import time
from time import sleep
import numpy
from pylsl import StreamInlet, resolve_stream

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



                with open('data.csv', 'a') as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                    info = {
                        "x_value": x_value,
                        "total_1": total_1,
                    }

                    csv_writer.writerow(info)
                    print(x_value, total_1)

                    x_value += 1
                    total_1 = sample[2] # <---- sample values from EMG-signal have to come here


                    time.sleep(0.005)
