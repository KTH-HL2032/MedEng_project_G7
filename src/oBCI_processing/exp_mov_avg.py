import numpy as np


class ExponentialMovingAverage:

    def get(self, interval, window):
        weights = np.exp(np.e(-1., 0., window))
        weights /= weights.sum()

        a = np.convolve(interval, weights)[:len(interval)]
        a[:window] = a[window]
        return a




