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

    def resize_horizontal(self):
        height = self.image.shape[1]
        width = round(self.image.shape[0] * 0.99)
        self.image = cv2.resize(self.image, (width, height))

    def resize_vertical(self):
        height = self.image.shape[0]
        width = round(self.image.shape[1] * 0.99)
        self.image = cv2.resize(self.image, (width, height))
