import numpy as np


class TiltDetector:
    cornerkeeper = None

    def __init__(self):
        self.cornerkeeper = [30]
        for i in range(0, 30):
            self.cornerkeeper.append(0)

    def update(self, corner):
        self.cornerkeeper.remove(self.cornerkeeper[0])
        self.cornerkeeper.append(corner)

    def LeftTilt(self):
        if 60 > np.mean(self.cornerkeeper) > 15:
            if not(np.mean(self.cornerkeeper[20:30]) < 15 or np.mean(self.cornerkeeper[20:30]) > 60):
                return True
        return False

    def RightTilt(self):
        if 120 < np.mean(self.cornerkeeper) < 165:
            if not(np.mean(self.cornerkeeper[20:30]) < 120 or np.mean(self.cornerkeeper[20:30]) > 165):
                return True
        return False

