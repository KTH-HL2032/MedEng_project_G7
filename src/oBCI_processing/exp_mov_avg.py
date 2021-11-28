import numpy as np
import time


class ExponentialMovingAverage:

    def __init__(self, size_max):
        self.w = [0]*size_max
        self.activated = False

    def get_old(self, interval, window):
        weights = np.exp(np.e(-1., 0., window))
        weights /= weights.sum()

        a = np.convolve(interval, weights)[:len(interval)]
        a[:window] = a[window]
        return a

    def get(self, interval, alpha, beta):

        for i in range(1,len(interval)):
            if interval[i] > interval[i-1]:
                self.w[i] = alpha*self.w[i-1] + (1-alpha)*interval[i]
            else:
                self.w[i] = beta*self.w[i-1] + (1-beta)*interval[i]
            if self.w[i] > 12:
                self.activated = True
                t1 = time.time()
                time_dif = 0
            else:
                self.activated = False
                time_dif = time.time()-t1


        return self.w, self.activated, time_dif

