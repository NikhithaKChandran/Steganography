import cv2
import os

from utils.file_utils import read_file, write_file, create_header, parse_header
from utils.binary_utils import bytes_to_binary
from utils.capacity import video_capacity
from utils.crypto_utils import encrypt, decrypt


# ----------------------------
# Encode Secret File into Video
# ----------------------------
def encode_video(cover_path, secret_path, output_path, key=None):

    cap = cv2.VideoCapture(cover_path)

    if not cap.isOpened():
        raise ValueError("Video could not be opened")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # read secret file
    data = read_file(secret_path)

    # create metadata header
    header = create_header(secret_path, data)
    payload = header + data

    # optional encryption
    if key:
        payload = encrypt(payload, key)

    binary_payload = bytes_to_binary(payload)

    data_index = 0
    data_len = len(binary_payload)

    success, frame = cap.read()

    if not success:
        raise ValueError("Video has no frames")

# capacity check
    capacity_per_frame = video_capacity(frame)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    total_capacity = capacity_per_frame * frame_count

    if len(binary_payload) > total_capacity * 8:
        raise ValueError("Secret file too large for this video")

    while success:

        for y in range(frame.shape[0]):
            for x in range(frame.shape[1]):

                pixel = frame[y, x]

                for channel in range(3):

                    if data_index < data_len:

                        bit = int(binary_payload[data_index])

                        pixel[channel] = (pixel[channel] & 254) | bit

                        data_index += 1

                frame[y, x] = pixel

                if data_index >= data_len:
                    break

            if data_index >= data_len:
                break

        out.write(frame)

        success, frame = cap.read()

    cap.release()
    out.release()

    return output_path


# ----------------------------
# Decode Secret File from Video
# ----------------------------
def decode_video(stego_path, output_folder, key=None):

    cap = cv2.VideoCapture(stego_path)

    if not cap.isOpened():
        raise ValueError("Video could not be opened")

    bits = []
    data_bytes = bytearray()

    header_found = False
    filename = None
    filesize = None
    header_end = None
    total_size = None

    success, frame = cap.read()

    while success:

        for y in range(frame.shape[0]):
            for x in range(frame.shape[1]):

                pixel = frame[y, x]

                for channel in range(3):

                    bits.append(str(pixel[channel] & 1))

                    if len(bits) == 8:

                        byte_value = int(''.join(bits), 2)
                        data_bytes.append(byte_value)
                        bits = []

                        # STEP 1: detect header
                        if not header_found and len(data_bytes) > 20:

                            try:
                                filename, filesize, header_end = parse_header(data_bytes)

                                total_size = header_end + filesize
                                header_found = True

                                print("Header found")
                                print("Filename:", filename)
                                print("Filesize:", filesize)

                            except:
                                pass

                        # STEP 2: stop when payload fully extracted
                        if header_found and len(data_bytes) >= total_size:

                            cap.release()

                            if key:
                                data_bytes = decrypt(data_bytes, key)

                            filename, filesize, header_end = parse_header(data_bytes)

                            file_data = data_bytes[header_end:header_end + filesize]

                            os.makedirs(output_folder, exist_ok=True)

                            output_path = os.path.join(output_folder, filename)

                            write_file(file_data, output_path)

                            print("Decoding completed successfully")

                            return output_path

        success, frame = cap.read()

    cap.release()

    raise ValueError("No hidden data found in video")