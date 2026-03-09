def image_capacity(img):

    height, width, channels = img.shape

    # total bits available (1 LSB per channel)
    total_bits = height * width * channels

    # convert bits → bytes
    capacity_bytes = total_bits // 8

    # reserve some space for metadata header
    capacity_bytes -= 100

    return capacity_bytes


def audio_capacity(frame_bytes):
    """
    Calculate maximum bytes that can be hidden in audio
    """

    bits = len(frame_bytes)

    return bits // 8


def video_capacity(frame):
    """
    Calculate capacity per video frame
    """

    height, width, channels = frame.shape

    bits = height * width * channels

    return bits // 8