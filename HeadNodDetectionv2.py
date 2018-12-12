import datetime
class nodDetector():
    movementcalculated = False
    mean = None
    timespan = 2
    start_time = None

    x_previous = None
    y_previous = None

    x_total = None
    y_total = None

    x_keeper = None
    y_keeper = None

    def __init__(self):
        self.x_keeper = []
        self.y_keeper = []
        self.start_time = datetime.datetime.now()

    def cleanUp(self, keeper):
        deleting = True
        while deleting and len(keeper) is not 0:
            time = self.getTimeNow()
            if time - keeper[0][0] > self.timespan:
                keeper.remove(keeper[0])
            else:
                deleting = False

    def update(self, faceObject):
        self.cleanUp(self.x_keeper)
        self.cleanUp(self.y_keeper)
        if self.x_previous is None:
            self.x_previous = faceObject.startX + faceObject.width/2
            self.y_previous = faceObject.startY + faceObject.height/2

        x_current = faceObject.startX + faceObject.width/2
        y_current = faceObject.startY + faceObject.height/2

        x_moved = 0
        y_moved = 0

        if 20 < abs(x_current - self.x_previous) < 300:
            x_moved = abs(x_current - self.x_previous)
        if 20 < abs(y_current - self.y_previous) < 300:
            y_moved = abs(y_current - self.y_previous)
        self.x_keeper.append((self.getTimeNow(), x_moved))
        self.y_keeper.append((self.getTimeNow(), y_moved))
        self.x_previous = x_current
        self.y_previous = y_current
        self.movementcalculated = False

    def getTimeNow(self):
        return (datetime.datetime.now() - self.start_time).total_seconds()

    def getNods(self):
        if not self.movementcalculated:
            x = 0
            for i in self.x_keeper:
                x = x + i[1]
            self.x_total = x
            y = 0
            for i in self.y_keeper:
                y = y + i[1]
            self.y_total = y

            self.movementcalculated = True

        yes = False
        no = False
        if self.y_total > 100 and self.y_total > self.x_total:
            yes = True
        elif self.x_total > 100 and self.x_total > self.y_total:
            no = True
        return no, yes
