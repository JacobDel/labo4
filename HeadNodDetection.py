class nodDetector():
    size = 41
    keeper = None

    def __init__(self):
        self.keeper = [self.size]
        for i in range(0, self.size):
            self.keeper.append((0,0))

    def update(self, faceObject):
        self.keeper.remove(self.keeper[0])
        x_previous, y_previous = self.keeper[len(self.keeper) - 1]
        x_current = faceObject.startX + faceObject.width/2
        y_current = faceObject.startY + faceObject.height/2

        if not 5< abs(x_current - x_previous) < 300:
            x_current = x_previous
        if not 5<abs(y_current - y_previous) < 300:
            y_current = y_previous
        self.keeper.append((x_current, y_current))

    def checknods(self):
        x_y_totals = [sum(x) for x in zip(*self.keeper)]
        vertical = False
        horizontal = False
        if x_y_totals[0] > 600 and x_y_totals[1] < 300:
            vertical = True
        elif x_y_totals[1] > 600 and x_y_totals[0] < 300:
            horizontal = True
        return horizontal, vertical
