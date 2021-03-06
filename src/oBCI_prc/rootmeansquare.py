import numpy
import math


class RootMeanSquare:

    def get(self, interval, halfwindow):
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
