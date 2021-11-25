import math
import sys

from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from pylsl import StreamInlet, resolve_stream
from time import sleep

import circbuffer
import rootmeansquare


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

rms = rootmeansquare.RootMeanSquare()
cbuffer = circbuffer.CircBuffer(size_max=512)
sendEverySmpl = math.ceil(inlet_sampleRate / outlet_sendRate)

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
        testval = rms.get(data_raw[:,2],64)

        if verbose:
            if samplesSent < 2:
                h1, = plt.plot(data_raw[:,2])
                h2, = plt.plot(testval)

            else:
                h1.set_ydata(data_raw[:,2])
                h2.set_ydata(testval)
            plt.pause(0.0000001)








