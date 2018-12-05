class Face:
    startX = 0
    startY = 0
    height = 0
    width = 0
    rightEyeX = None
    rightEyeY = None
    rightEyeWidth = None
    rightEyeHeight = None
    leftEyeY = None
    leftEyeX = None
    leftEyeHeight = None
    leftEyeWidth = None
    smileX = None
    smileY = None
    smileWidth = None
    smileHeight = None

    def __init__(self, x, y, h, w):
        # ,leftEyeX,leftEyeY,rightEyeX,rightEyeY,leftEyeWidth,leftEyeHeight
        self.startX = x
        self.startY = y
        self.width = w
        self.height = h
        # self.rightEyeX = rightEyeX
        # self.leftEyeX = leftEyeX
        # self.rightEyeY = rightEyeY
        # self.leftEyeY = leftEyeY
        # self.leftEyeWidth = leftEyeWidth
        # self.rightEyeWidth = leftEyeHeight

    def setHead(self, i_startX, i_startY, i_width, i_height):
        self.startX = i_startX
        self.startY = i_startY
        self.width = i_width
        self.height = i_height

    def setRightEye(self, i_righteyeX, i_righteyeY, i_righteyewidth, i_righteyeheight):
        self.rightEyeX = i_righteyeX
        self.rightEyeY = i_righteyeY
        self.rightEyeWidth = i_righteyewidth
        self. rightEyeHeight = i_righteyeheight

    def setLeftEye(self, i_lefteyeX, i_lefteyeY, i_lefteyewidth, i_lefteyeheight):
        self.rightEyeX = i_lefteyeX
        self.rightEyeY = i_lefteyeY
        self.rightEyeWidth = i_lefteyewidth
        self. rightEyeHeight = i_lefteyeheight