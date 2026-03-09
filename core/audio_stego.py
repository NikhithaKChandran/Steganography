import wave
import os

from utils.file_utils import read_file, write_file, create_header, parse_header
from utils.binary_utils import bytes_to_binary, binary_to_bytes
from utils.capacity import audio_capacity
from utils.crypto_utils import encrypt, decrypt


# ----------------------------
# Encode Secret File into Audio
# ----------------------------
def encode_audio(cover_path, secret_path, output_path, key=None):

    # open audio file
    with wave.open(cover_path, 'rb') as song:

        params = song.getparams()
        frames = bytearray(song.readframes(song.getnframes()))

    # read secret file
    data = read_file(secret_path)

    # create metadata header
    header = create_header(secret_path, data)

    payload = header + data

    # optional encryption
    if key:
        payload = encrypt(payload, key)

    # capacity check
    capacity = audio_capacity(frames)

    if len(payload) > capacity:
        raise ValueError("Secret file too large for this audio")

    binary_payload = bytes_to_binary(payload)

    data_index = 0
    data_len = len(binary_payload)

    # embed bits in audio frames
    for i in range(len(frames)):

        if data_index < data_len:

            bit = int(binary_payload[data_index])

            frames[i] = (frames[i] & 254) | bit

            data_index += 1

        else:
            break

    # write stego audio
    with wave.open(output_path, 'wb') as stego:

        stego.setparams(params)
        stego.writeframes(bytes(frames))

    return output_path


# ----------------------------
# Decode Secret File from Audio
# ----------------------------
def decode_audio(stego_path, output_folder, key=None):

    with wave.open(stego_path, 'rb') as song:
        frames = bytearray(song.readframes(song.getnframes()))

    bits = []
    data_bytes = bytearray()

    for byte in frames:

        bits.append(str(byte & 1))

        if len(bits) == 8:

            byte_value = int(''.join(bits), 2)
            data_bytes.append(byte_value)
            bits = []

            # once header is readable, stop after full payload
            if b'|' in data_bytes:
                try:
                    filename, filesize, header_end = parse_header(data_bytes)

                    total_size = header_end + filesize

                    if len(data_bytes) >= total_size:
                        break

                except:
                    pass

    # decrypt if needed
    if key:
        data_bytes = decrypt(data_bytes, key)

    # parse metadata
    filename, filesize, header_end = parse_header(data_bytes)

    file_data = data_bytes[header_end:header_end + filesize]

    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, filename)

    write_file(file_data, output_path)

    return output_path