import math
import sys
import time

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from pylsl import StreamInlet, resolve_stream

import circbuffer
import rootmeansquare
import exp_mov_avg


class Processing:

    def __innit__(self, channel):
        self.verbose = False
        output_width = 32
        output_height = 32
        output_stacks = 3
        self.outlet_sendRate = 2

        self.buffer_size = 128

        self.muscle_activated = False
        self.time_diff = 0
        self.T1 = 0
        self.T2 = 0
        self.flag_entry = 1
        self.flag_exit = 1

    def connect_stream(self):
        print("looking for an EMG stream...")
        streams = resolve_stream('type', 'EMG')
        self.inlet = StreamInlet(streams[0])

        in_let_info = self.inlet.info()

        self.inlet_sample_rate = int(in_let_info.nominal_srate())
        inlet_num_channels = int(in_let_info.channel_count())
        if self.verbose:
            print("Reported sample rate: %i , number of channels: %i" % (self.inlet_sample_rate, inlet_num_channels))

    def processing(self):

        Processing.connect_stream(self)

        ema = exp_mov_avg.ExponentialMovingAverage(self.buffer_size)
        rms = rootmeansquare.RootMeanSquare()
        cbuffer = circbuffer.CircBuffer(self.buffer_size)
        send_every_smpl = math.ceil(self.inlet_sample_rate / self.outlet_sendRate)

        samples_in_buffer = 0
        samples_sent = 0

        if self.verbose:
            fig = plt.figure(figsize=(10, 8))
            outer = gridspec.GridSpec(3, 1, wspace=0, hspace=0.2)


            class closer:
                def __init__(self):
                    self.run = True

                def handle_close(self, evt):
                    print('\nClosed figure, shutting down')
                    self.run = False


            obs = closer()
            fig.canvas.mpl_connect('close_event', obs.handle_close)
            print("Close the figure to stop the application.")
        else:
            class Closer:
                def __init__(self):
                    self.run = True

            obs = Closer()

        while obs.run:
            cbuffer.append(self.inlet.pull_sample()[0])
            samples_in_buffer += 1

            if cbuffer.full and samples_in_buffer >= send_every_smpl:
                data_raw = np.array(cbuffer.get())[:, 0:3]

                samples_sent += 1
                samples_in_buffer = 0
                data_rms = rms.get(data_raw[:, 2], 128)
                data_ema, self.muscle_activated = ema.get(data_rms, 0.9, 0.9)
                sys.stdout.write(
                    '\r samples sent: %i muscle activated: %s Time difference: %f' % (samples_sent, self.muscle_activated, self.time_diff))

                if self.muscle_activated and self.flag_entry == 1:
                    self.T1 = time.time()
                    self.flag_entry = 0
                    self.flag_exit = 1

                elif not self.muscle_activated and self.flag_exit == 1:
                    self.T2 = time.time()
                    self.time_diff = self.T2 - self.T1
                    self.flag_entry = 1
                    self.flag_exit = 0

                if self.verbose:
                    if samples_sent < 2:
                        h1, = plt.plot(data_raw[:, 2])
                        h2, = plt.plot(data_rms)
                        h3, = plt.plot(data_ema)

                    else:
                        h1.set_ydata(data_raw[:, 2])
                        h2.set_ydata(data_rms)
                        h3.set_ydata(data_ema)
                    plt.pause(0.0000001)

        return self.time_diff
