import csv
import random
import time
from pylsl import StreamInlet, resolve_stream
from time import sleep
import numpy

x_value = 0
total_1 = 0


fieldnames = ["x_value", "total_1"]


with open('data_sets/data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('data_sets/data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "total_1": total_1,
        }

        csv_writer.writerow(info)
        print(x_value, total_1)

        x_value += 1
        total_1 = total_1 + 5 # <---- sample values from EMG-signal have to come here


    time.sleep(0.005)

