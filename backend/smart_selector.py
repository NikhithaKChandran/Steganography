import cv2
import numpy as np

def analyze_image(img):

    height,width,_ = img.shape

    capacity = (height * width * 3) // 8

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    variance = np.var(gray)

    score = variance / 1000

    return {
        "capacity": capacity,
        "score": round(score,2)
    }