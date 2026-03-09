import cv2

from utils import capacity
from utils.file_utils import read_file, write_file, create_header, parse_header
from utils.binary_utils import bytes_to_binary, binary_to_bytes
from utils.capacity import image_capacity
from utils.crypto_utils import encrypt, decrypt

# ----------------------------
# Encode Secret File into Image
# ----------------------------
def encode_image(cover_path, secret_path, output_path, key=None):

    img = cv2.imread(cover_path)

    if img is None:
        raise ValueError("Cover image could not be loaded")

    # read secret file
    data = read_file(secret_path)

    # add metadata header
    header = create_header(secret_path, data)
    payload = header + data

    # optional encryption
    if key:
        payload = encrypt(payload, key)

    # capacity check
    capacity = image_capacity(img)

    if len(payload) > capacity:
        print("Payload size:", len(payload))
        print("Image capacity:", capacity)
        raise ValueError("Secret file too large for this image")

    binary_payload = bytes_to_binary(payload)

    data_index = 0
    data_len = len(binary_payload)

    height, width, _ = img.shape

    for y in range(height):
        for x in range(width):
            pixel = img[y, x]

            for channel in range(3):

                if data_index < data_len:
                    bit = int(binary_payload[data_index])

                    pixel[channel] = (pixel[channel] & 254) | bit

                    data_index += 1

            img[y, x] = pixel

            if data_index >= data_len:
                break

        if data_index >= data_len:
            break

    cv2.imwrite(output_path, img)

    return output_path


# ----------------------------
# Decode Secret File from Image
# ----------------------------
def decode_image(stego_path, output_folder, key=None):

    img = cv2.imread(stego_path)

    if img is None:
        raise ValueError("Stego image could not be loaded")

    bits = []

    height, width, _ = img.shape

    for y in range(height):
        for x in range(width):
            pixel = img[y, x]

            for channel in range(3):
                bits.append(str(pixel[channel] & 1))

    binary_data = ''.join(bits)

    data_bytes = binary_to_bytes(binary_data)

    # decrypt if needed
    if key:
        data_bytes = decrypt(data_bytes, key)

    filename, filesize, header_end = parse_header(data_bytes)

    file_data = data_bytes[header_end:header_end + filesize]

    output_path = f"{output_folder}/{filename}"

    write_file(file_data, output_path)

    return output_path