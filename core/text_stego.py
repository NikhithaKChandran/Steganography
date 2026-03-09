import os
from utils.binary_utils import bytes_to_binary, binary_to_bytes
from utils.file_utils import read_file, write_file
from utils.file_utils import read_file, write_file, create_header, parse_header
from utils.crypto_utils import encrypt, decrypt

# Zero-width characters
ZW_SPACE = '\u200B'   # 0
ZW_NONJOIN = '\u200C' # 1
END_MARKER = '\u200D'


def encode_text(cover_text, file_path, key=None):

    # Read file
    file_data = read_file(file_path)

    filename = os.path.basename(file_path)

    header = create_header(file_path, file_data)

    payload = header + file_data

    # Encrypt if key provided
    if key:
        payload = encrypt(payload, key)

    binary_payload = bytes_to_binary(payload)

    # Convert bits to zero-width characters
    hidden_chars = []

    for bit in binary_payload:
        if bit == '0':
            hidden_chars.append(ZW_SPACE)
        else:
            hidden_chars.append(ZW_NONJOIN)

    hidden_string = ''.join(hidden_chars) + END_MARKER

    # Embed hidden data at end of text
    stego_text = cover_text + hidden_string

    return stego_text


def decode_text(stego_text, output_folder="output", key=None):

    bits = []

    for char in stego_text:

        if char == ZW_SPACE:
            bits.append('0')

        elif char == ZW_NONJOIN:
            bits.append('1')
        elif char == END_MARKER:
            break

    if not bits:
        raise ValueError("No hidden data found")

    binary_data = ''.join(bits)

    data_bytes = binary_to_bytes(binary_data)

    # Decrypt if needed
    if key:
        data_bytes = decrypt(data_bytes, key)

    # Parse metadata header
    filename, filesize, header_end = parse_header(data_bytes)

    file_data = data_bytes[header_end:header_end + filesize]

    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, "decoded_" + filename)

    write_file(file_data, output_path)

    return output_path