import datetime

"""
tiltdetector is not used, it only worked with camshift
"""
class TiltDetector:
    meancalculated = False
    mean = None
    cornerkeeper = None
    timespan = 1
    start_time = None
    def __init__(self):
        self.cornerkeeper = []
        self.start_time = datetime.datetime.now()
        # for i in range(0, 40):
        #     self.cornerkeeper.append((self.getTimeNow(), 0))

    def getTimeNow(self):
        return (datetime.datetime.now() - self.start_time).total_seconds()

    def update(self, corner):
        deleting = True
        while deleting and len(self.cornerkeeper) is not 0:
            if self.getTimeNow() - self.cornerkeeper[0][0] > self.timespan:
                self.cornerkeeper.remove(self.cornerkeeper[0])
            else:
                deleting = False
        self.cornerkeeper.append((self.getTimeNow(), corner))
        self.meancalculated = False

    def LeftTilt(self):
        if 60 > self.Getaverage() > 20:
            return True
        return False

    def RightTilt(self):
        if 120 < self.Getaverage() < 160:
            return True
        return False

    def Getaverage(self):
        if not self.meancalculated:
            sum = 0
            for i in self.cornerkeeper:
                sum = sum + i[1]
            self.mean = sum/len(self.cornerkeeper)
            self.meancalculated = True
        return self.mean

