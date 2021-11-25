import numpy as np


class Exponential_Moving_Average:

    def ExpMovingAverage(self,window):
        weights = np.exp(np.linespace(-1., 0., window))
        weights /= weights.sum()

        a = np.convolve(self, weights)[:len(self)]
        a[:window] = a[window]
        return a




