import numpy as np
class Isl:
    def __int__(self, start, end, speed_rate):
        self.start = start
        self.end = end
        self.speed_rate = speed_rate

    def get_length(self, t):
        return np.linalg.norm(self.start.get_xyz(t) - self.end.get_xyz(t))
