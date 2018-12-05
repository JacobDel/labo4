class Face:
    startX = 0
    startY = 0
    height = 0
    width = 0
    rightEyeX = None
    rightEyeY = None
    leftEyeY = None
    leftEyeX = None
    eyeHeight = None
    eyeWidth = None
    smileX = None
    smileY = None
    smileWidth = None
    smileHeight = None

    def __init__(self, x, y, h, w):
        self.startX = x
        self.startY = y
        self.width = w
        self.height = h

    def setHead(self, i_startX, i_startY, i_width, i_height):
        self.startX = i_startX
        self.startY = i_startY
        self.width = i_width
        self.height = i_height

    def setEyes(self, i_lefteyeX, i_lefteyeY, i_righteyeX, i_righteyeY, i_width, i_height):
        self.leftEyeX = i_lefteyeX
        self.leftEyeY = i_lefteyeY
        self.eyeHeight = i_height
        self.eyeWidth = i_width
        self.rightEyeY = i_righteyeY
        self.rightEyeX = i_righteyeX