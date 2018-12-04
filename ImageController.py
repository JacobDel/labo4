import cv2

class image_controller:
    image = None
    image_original = None

    def __init__(self, i_image):
        self.image = i_image
        self.image_original = i_image

    def rotate(self, angle):
        M = cv2.getRotationMatrix2D((self.image.shape[1]/2, self.image.shape[0]/2), angle, 1)
        self.image = cv2.warpAffine(self.image, M, (self.image.shape[1], self.image.shape[0]))

    def reset(self):
        self.image = self.image_original

    def show(self):
        cv2.imshow('control this image!', self.image)
