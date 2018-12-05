class nodDetector():
    size = 41
    x_keeper = None
    y_keeper = None

    x_previous = None
    y_previous  = None

    def __init__(self):
        self.x_keeper = [self.size]
        self.y_keeper = [self.size]
        for i in range(0, self.size):
            self.x_keeper.append(0)
            self.y_keeper.append(0)

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