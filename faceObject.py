class Face:
    startX=0
    startY = 0
    height = 0
    width = 0
    rightEyeX = None
    rightEyeY = None
    leftEyeY =None
    leftEyeX = None
    leftEyeHeight =None
    leftEyeWidth =None
    smileX = None
    smileY = None
    smileWidth = None
    smileHeight = None
    def __init__(self,x,y,h,w):
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