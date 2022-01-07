class CircBuffer:

    def __init__(self, size_max):
        self.max = size_max
        self.data = []
        self.full = False

    class __Full:
        """ class that implements a full buffer """
        def append(self, x):
            self.data[self.cur] = x
            self.cur = int((self.cur+1) % self.max)

        def get(self):
            return self.data[self.cur:]+self.data[:self.cur]

    def append(self,x):
        """ append an element at the end of the buffer """
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self.__Full
            self.full = True

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data
