import numpy as np
import cv2
import wave


# ---------------------------
# Binary Conversion
# ---------------------------

def msgtobinary(msg):

    if type(msg) == str:
        return ''.join(format(ord(i), "08b") for i in msg)

    elif type(msg) == bytes or type(msg) == np.ndarray:
        return [format(i, "08b") for i in msg]

    elif type(msg) == int or type(msg) == np.uint8:
        return format(msg, "08b")

    else:
        raise TypeError("Unsupported type")


# ---------------------------
# IMAGE STEGANOGRAPHY
# ---------------------------

def encode_image(img, message):

    message += "*^*^*"

    binary_data = msgtobinary(message)
    data_len = len(binary_data)
    index = 0

    for row in img:
        for pixel in row:

            r,g,b = msgtobinary(pixel)

            if index < data_len:
                pixel[0] = int(r[:-1] + binary_data[index],2)
                index += 1

            if index < data_len:
                pixel[1] = int(g[:-1] + binary_data[index],2)
                index += 1

            if index < data_len:
                pixel[2] = int(b[:-1] + binary_data[index],2)
                index += 1

            if index >= data_len:
                return img

    return img


def decode_image(img):

    binary_data=""

    for row in img:
        for pixel in row:

            r,g,b = msgtobinary(pixel)

            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]

    all_bytes=[binary_data[i:i+8] for i in range(0,len(binary_data),8)]

    decoded=""

    for byte in all_bytes:

        decoded += chr(int(byte,2))

        if decoded.endswith("*^*^*"):
            return decoded[:-5]

    return ""


# ---------------------------
# AUDIO STEGANOGRAPHY
# ---------------------------

def encode_audio(audio_path,message,outfile):

    song = wave.open(audio_path,'rb')

    frames = song.readframes(song.getnframes())
    frame_bytes = bytearray(frames)

    message += "*^*^*"

    bits = list(map(int,''.join(format(ord(i),'08b') for i in message)))

    for i,bit in enumerate(bits):

        frame_bytes[i] = (frame_bytes[i] & 254) | bit

    frame_modified = bytes(frame_bytes)

    with wave.open(outfile,'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)

    return outfile


def decode_audio(audio_path):

    song = wave.open(audio_path,'rb')

    frame_bytes = bytearray(song.readframes(song.getnframes()))

    extracted=""

    for byte in frame_bytes:

        extracted += str(byte & 1)

    all_bytes=[extracted[i:i+8] for i in range(0,len(extracted),8)]

    decoded=""

    for byte in all_bytes:

        decoded += chr(int(byte,2))

        if decoded.endswith("*^*^*"):
            return decoded[:-5]

    return ""


# ---------------------------
# VIDEO STEGANOGRAPHY
# ---------------------------

def encode_video(video_path,message,outfile):

    cap=cv2.VideoCapture(video_path)

    fourcc=cv2.VideoWriter_fourcc(*'XVID')

    width=int(cap.get(3))
    height=int(cap.get(4))

    out=cv2.VideoWriter(outfile,fourcc,25,(width,height))

    message += "*^*^*"

    binary_data = msgtobinary(message)
    index=0

    while True:

        ret,frame=cap.read()

        if not ret:
            break

        for row in frame:
            for pixel in row:

                r,g,b = msgtobinary(pixel)

                if index < len(binary_data):
                    pixel[0] = int(r[:-1] + binary_data[index],2)
                    index+=1

                if index < len(binary_data):
                    pixel[1] = int(g[:-1] + binary_data[index],2)
                    index+=1

                if index < len(binary_data):
                    pixel[2] = int(b[:-1] + binary_data[index],2)
                    index+=1

        out.write(frame)

    cap.release()
    out.release()

    return outfile


# ---------------------------
# TEXT STEGANOGRAPHY
# ---------------------------

def encode_text(cover_file,message,output):

    with open(cover_file,"r") as f:
        words=f.read().split()

    message += "#####"

    binary = ''.join(format(ord(i),'08b') for i in message)

    encoded_words=[]

    for i,word in enumerate(words):

        if i < len(binary):
            encoded_words.append(word + chr(8203))
        else:
            encoded_words.append(word)

    with open(output,"w",encoding="utf-8") as f:
        f.write(" ".join(encoded_words))

    return output