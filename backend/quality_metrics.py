import numpy as np
import cv2

def calculate_metrics(original, encoded):

    mse = np.mean((original - encoded) ** 2)

    if mse == 0:
        psnr = 100
    else:
        psnr = 20 * np.log10(255.0 / np.sqrt(mse))

    return {
        "mse": float(mse),
        "psnr": float(psnr)
    }
