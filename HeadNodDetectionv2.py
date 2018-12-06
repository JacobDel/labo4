import datetime
class nodDetector():
    movementcalculated = False
    mean = None
    keeper = None
    timespan = 1
    start_time = None
    previous = None

    x_keeper = None
    y_keeper = None

    def __init__(self):
        self.keeper = []
        self.start_time = datetime.datetime.now()

    def update(self, faceObject):
        if self.x_previous is None:
            self.x_previous = faceObject.startX + faceObject.width/2
            self.y_previous = faceObject.startY + faceObject.height/2
        self.x_keeper.remove(self.x_keeper[0])
        self.y_keeper.remove(self.y_keeper[0])

        x_current = faceObject.startX + faceObject.width/2
        y_current = faceObject.startY + faceObject.height/2

        x_moved = 0
        y_moved = 0

        if 5 < abs(x_current - self.x_previous) < 300:
            x_moved = abs(x_current - self.x_previous)
        if 5 < abs(y_current -self.y_previous) < 300:
            y_moved = abs(y_current - self.y_previous)
        self.x_keeper.append(x_moved)
        self.y_keeper.append(y_moved)
        self.x_previous = x_current
        self.y_previous = y_current

        self.movementcalculated = False

    def checknods(self):
        vertical = False
        horizontal = False
        if sum(self.x_keeper) > 400 and sum(self.y_keeper) < 300:
            vertical = True
        elif sum(self.y_keeper) > 300 and sum(self.x_keeper) < 200:
            horizontal = True
        return horizontal, vertical

    def get_values(self):
        return str(sum(self.x_keeper)), str(sum(self.y_keeper))

    def getTimeNow(self):
        return (datetime.datetime.now() - self.start_time).total_seconds()

    def cleanUp(self):
        deleting = True
        while deleting and len(self.keeper) is not 0:
            if self.getTimeNow() - self.keeper[0][0] > self.timespan:
                self.keeper.remove(self.keeper[0])
            else:
                deleting = False

    def Getaverage(self):
        if not self.movementcalculated:
            sum_x = 0
            sum_y = 0
            for i in self.cornerkeeper:
                sum_x = sum_x + i[1]
                sum_y = sum_y + i[2]




            self.mean = sum/len(self.cornerkeeper)
            self.meancalculated = True
        return self.mean




import datetime


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

    def cleanUp(self):
        deleting = True
        while deleting and len(self.cornerkeeper) is not 0:
            if self.getTimeNow() - self.cornerkeeper[0][0] > self.timespan:
                self.cornerkeeper.remove(self.cornerkeeper[0])
            else:
                deleting = False

    def update(self, corner):
        self.cleanUp()
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
        self.cleanUp()
        if not self.meancalculated:
            sum = 0
            for i in self.cornerkeeper:
                sum = sum + i[1]
            self.mean = sum/len(self.cornerkeeper)
            self.meancalculated = True
        return self.mean

