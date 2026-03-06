import cv2
import numpy as np

def detect_steganography(img):

    lsb_values = []

    for row in img:
        for pixel in row:
            for value in pixel:
                lsb_values.append(value & 1)

    lsb_values = np.array(lsb_values)

    ratio = np.mean(lsb_values)

    probability = abs(0.5 - ratio) * 2

    return round(probability,2)