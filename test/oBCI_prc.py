import math
import sys
import time

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from pylsl import StreamInlet, resolve_stream

import src.oBCI_prc.circbuffer as circbuffer
import src.oBCI_prc.rootmeansquare as rootmeansquare
import src.oBCI_prc.expmovavg as expmovavg

# ============================================================================
# PARAMETERS
# ============================================================================
# 0. General
verbose = False
# 1. Output
output_width    = 32
output_height   = 32
output_stacks   = 3  # channels
outlet_sendRate = 2 # [Hz]

buffer_size = 128

muscle_activated = False
time_diff = 0
T1 = 0
T2 = 0
flag_entry = 1
flag_exit = 1
counter = 0

# ============================================================================
# PROCESS
# ============================================================================

print("looking for an EMG stream...")
streams = resolve_stream('type', 'EMG')
inlet = StreamInlet(streams[0])

inletInfo = inlet.info()

inlet_sampleRate = int(inletInfo.nominal_srate())
inlet_numChannels = int(inletInfo.channel_count())
if verbose:
    print("Reported sample rate: %i , number of channels: %i" %(inlet_sampleRate, inlet_numChannels))

# ============================================================================
#INIT
ema = expmovavg.ExpMovAvg(buffer_size)
rms = rootmeansquare.RootMeanSquare()
cbuffer = circbuffer.CircBuffer(buffer_size)
sendEverySmpl = math.ceil(inlet_sampleRate / outlet_sendRate)
# ============================================================================

samplesInBuffer = 0
samplesSent = 0

if verbose:
    fig = plt.figure(figsize=(10,8))
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
    cbuffer.append(inlet.pull_sample()[0])
    samplesInBuffer += 1

    if(cbuffer.full and samplesInBuffer>=sendEverySmpl):
        data_raw = np.array(cbuffer.get())[:,0:3]

        samplesSent += 1
        samplesInBuffer = 0
        data_rms = rms.get(data_raw[:,2],128)
        data_ema, muscle_activated = ema.get(data_rms,0.9,0.9)
        sys.stdout.write('\rsamples sent: %i muscle activated: %s Time difference: %f' % (samplesSent, muscle_activated, time_diff))

        if muscle_activated == True and flag_entry == 1:
            T1 = time.time()
            flag_entry = 0
            flag_exit = 1

        elif muscle_activated == False and flag_exit ==1:
            if counter > 0:
                T2 = time.time()
                time_diff = T2-T1
            flag_entry = 1
            flag_exit = 0
            counter += 1

        if verbose:
            if samplesSent < 2:
                h1, = plt.plot(data_raw[:,2])
                h2, = plt.plot(data_rms)
                h3, = plt.plot(data_ema)

            else:
                h1.set_ydata(data_raw[:,2])
                h2.set_ydata(data_rms)
                h3.set_ydata(data_ema)
            plt.pause(0.0000001)








