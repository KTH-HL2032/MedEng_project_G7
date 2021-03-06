import numpy as np


class ExpMovAvg:

    def __init__(self, size_max):
        self.w = [0]*size_max
        self.activated = False

    def get(self, interval, alpha, beta):

        for i in range(1, len(interval)):
            if interval[i] > interval[i-1]:
                self.w[i] = alpha*self.w[i-1] + (1-alpha)*interval[i]
            else:
                self.w[i] = beta*self.w[i-1] + (1-beta)*interval[i]

        avg_w = sum(self.w)/len(self.w)
        if avg_w > 53:
            self.activated = True

        else:
            self.activated = False

        return self.w, self.activated
