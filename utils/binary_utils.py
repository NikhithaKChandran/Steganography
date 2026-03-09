def bytes_to_binary(data):
    """Convert bytes to binary string"""
    return ''.join(format(byte, '08b') for byte in data)


def binary_to_bytes(binary):
    """Convert binary string back to bytes"""

    byte_array = bytearray()

    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]

        if len(byte) == 8:
            byte_array.append(int(byte, 2))

    return bytes(byte_array)


def msg_to_binary(data):
    """
    Convert different data types to binary
    Used for pixels, frames, and small values
    """

    if isinstance(data, str):
        return ''.join(format(ord(i), '08b') for i in data)

    elif isinstance(data, (bytes, bytearray)):
        return [format(i, '08b') for i in data]

    elif isinstance(data, int):
        return format(data, '08b')

    else:
        raise TypeError("Unsupported data type")