import numpy as np

overshoot = 0.5

# eyesframeMHIs = MHI picture of the eyes
def getWinkRecognition(eyesFrameMHI):
    global overshoot
    #calulate ratio of white pixels in the black eyesFrameMHI
    n_white_pix = np.sum(eyesFrameMHI == 255)
    amountOfPixels = len(eyesFrameMHI)*len(eyesFrameMHI[0])
    if n_white_pix/amountOfPixels > overshoot:
        return True
    else:
        return False