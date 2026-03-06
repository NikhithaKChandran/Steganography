import cv2
import numpy as np


# Convert text to binary
def text_to_binary(text):
    return ''.join(format(ord(i), '08b') for i in text)


# Encode secret data into image
def encode_image(img, data):

    data += "#####"
    binary_data = text_to_binary(data)
    data_index = 0
    data_length = len(binary_data)

    for row in img:
        for pixel in row:

            for i in range(3):

                if data_index < data_length:

                    # Clear last bit and insert message bit safely
                    pixel[i] = (pixel[i] & 254) | int(binary_data[data_index])

                    data_index += 1

                else:
                    return img

    return img


# Decode secret data from image
def decode_image(img):

    binary_data = ""

    for row in img:
        for pixel in row:
            for i in range(3):
                binary_data += str(pixel[i] & 1)

    # Split binary into bytes
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]

    decoded = ""

    for byte in all_bytes:

        decoded += chr(int(byte, 2))

        if decoded.endswith("#####"):
            return decoded[:-5]

    return ""