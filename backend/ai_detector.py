import cv2
import numpy as np

def detect_steganography(img):

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Calculate noise using Laplacian variance
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    # Extract LSB plane
    lsb_plane = gray & 1

    # Calculate randomness of LSB
    lsb_mean = np.mean(lsb_plane)

    # Heuristic probability calculation
    probability = (lsb_mean + (laplacian_var / 1000)) / 2

    # Normalize between 0 and 1
    probability = min(max(probability, 0), 1)

    return float(probability)
