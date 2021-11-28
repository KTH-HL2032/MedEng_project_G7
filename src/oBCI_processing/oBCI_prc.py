import math
import sys

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from pylsl import StreamInlet, resolve_stream
from time import sleep

import circbuffer
import rootmeansquare
import exp_mov_avg


# ============================================================================
# PARAMETERS
# ============================================================================
# 0. General
verbose = True
# 1. Output
output_width    = 32
output_height   = 32
output_stacks   = 3  # channels
outlet_sendRate = 2 # [Hz]

buffer_size=1024

muscle_activated = False
time_difference  = 0

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
ema = exp_mov_avg.ExponentialMovingAverage(buffer_size)
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
    class closer:
        def __init__(self):
            self.run = True

    obs = closer()

while obs.run:
    cbuffer.append(inlet.pull_sample()[0])
    samplesInBuffer += 1

    if(cbuffer.full and samplesInBuffer>=sendEverySmpl):
        data_raw = np.array(cbuffer.get())[:,0:3]

        samplesSent += 1
        sys.stdout.write('\rsamples sent: %i' % samplesSent)  # \r requires stdout to work
        samplesInBuffer = 0
        data_rms = rms.get(data_raw[:,2],128)
        data_ema, muscle_activated, time_difference = ema.get(data_rms,0.9,0.9)
        sys.stdout.write('\rmuscle activated: %s' % muscle_activated)
        sys.stdout.write('\rtime difference: %s' % time_difference)

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








