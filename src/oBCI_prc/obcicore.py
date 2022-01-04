import math
import time

from matplotlib import pyplot as plt
from matplotlib import gridspec
import numpy as np
from pylsl import StreamInlet, resolve_stream

from src.oBCI_prc.circbuffer import CircBuffer
from src.oBCI_prc.rootmeansquare import RootMeanSquare
from src.oBCI_prc.expmovavg import ExpMovAvg


class ObciCore:

    def __init__(self):
        self.verbose = False
        self.output_width = 32
        self.output_height = 32
        self.output_stacks = 3
        self.outlet_sendRate = 2
        self.number = 0

        self.robot_activated_2 = False
        self.robot_activated_3 = False

        self.buffer_size = 128

        self.muscle_activated_2 = False
        self.muscle_activated_3 = False

        self.time_diff_2 = 0
        self.time_diff_3 = 0
        self.time_list = [0]*3

        self.T1_2 = 0
        self.T2_2 = 0
        self.T1_3 = 0
        self.T2_3 = 0
        self.flag_entry_2 = 1
        self.flag_exit_2 = 1
        self.flag_entry_3 = 1
        self.flag_exit_3 = 1

        self.counter_2 = 0
        self.counter_3 = 0

    def processing(self):

        # print("looking for an EMG stream...")
        streams = resolve_stream('type', 'EMG')
        self.inlet = StreamInlet(streams[0])

        in_let_info = self.inlet.info()

        self.inlet_sample_rate = int(in_let_info.nominal_srate())
        self.inlet_num_channels = int(in_let_info.channel_count())
        # if self.verbose:
        # print("Reported sample rate: %i , number of channels: %i" % (self.inlet_sample_rate, self.inlet_num_channels))

        ema = ExpMovAvg(self.buffer_size)
        rms = RootMeanSquare()
        cbuffer = CircBuffer(self.buffer_size)
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
                    # print('\nClosed figure, shutting down')
                    self.run = False

            obs = closer()
            fig.canvas.mpl_connect('close_event', obs.handle_close)
            # print("Close the figure to stop the application.")
        else:
            class Closer:
                def __init__(self):
                    self.run = True

            obs = Closer()

        while obs.run:
            start_time_loop = time.time()
            cbuffer.append(self.inlet.pull_sample()[0])
            samples_in_buffer += 1

            if cbuffer.full and samples_in_buffer >= send_every_smpl:
                data_raw = np.array(cbuffer.get())[:, 0:3]

                samples_sent += 1
                samples_in_buffer = 0

                data_rms_2 = rms.get(data_raw[:, 1], 128)
                data_rms_3 = rms.get(data_raw[:, 2], 128)

                data_ema_2, self.muscle_activated_2 = ema.get(data_rms_2, 0.9, 0.9)
                data_ema_3, self.muscle_activated_3 = ema.get(data_rms_3, 0.9, 0.9)

                if self.muscle_activated_2 and self.flag_entry_2 == 1:
                    self.T1_2 = time.time()
                    self.flag_entry_2 = 0
                    self.flag_exit_2 = 1

                elif not self.muscle_activated_2 and self.flag_exit_2 == 1:
                    if self.counter_2 > 0:
                        self.T2_2 = time.time()
                        self.time_diff_2 = self.T2_2-self.T1_2
                    self.flag_entry_2 = 1
                    self.flag_exit_2 = 0
                    self.counter_2 += 1

                if self.muscle_activated_3 and self.flag_entry_3 == 1:
                    self.T1_3 = time.time()
                    self.flag_entry_3 = 0
                    self.flag_exit_3 = 1

                elif not self.muscle_activated_3 and self.flag_exit_3 == 1:
                    if self.counter_3 > 0:
                        self.T2_3 = time.time()
                        self.time_diff_3 = self.T2_3-self.T1_3
                    self.flag_entry_3 = 1
                    self.flag_exit_3 = 0
                    self.counter_3 += 1

                self.number += 1

                end_time_loop = time.time()
                # TODO: replace loop time with a flag (attribute) and methods to set the attribute
                loop_time = end_time_loop - start_time_loop

                yield self.time_diff_2, self.time_diff_3, self.muscle_activated_2, self.muscle_activated_3, loop_time

                self.time_diff_2 = 0
                self.time_diff_3 = 0
