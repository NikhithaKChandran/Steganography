import os

from core.image_stego import encode_image, decode_image
from core.video_stego import encode_video, decode_video
from core.audio_stego import encode_audio, decode_audio
from core.text_stego import encode_text, decode_text


def encode_nested(secret_file, layers, output_folder):

    current_payload = secret_file
    stego_path = None

    os.makedirs(output_folder, exist_ok=True)

    # start from innermost layer
    for i in reversed(range(len(layers))):

        layer = layers[i]
        layer_type = layer["type"]
        cover = layer["cover"]
        key = layer["key"]

        stego_path = os.path.join(output_folder, f"layer_{i+1}_stego")

        if layer_type == "image":
            stego_path += ".png"
            encode_image(cover, current_payload, stego_path, key)

        elif layer_type == "video":
            stego_path += ".mp4"
            encode_video(cover, current_payload, stego_path, key)

        elif layer_type == "audio":
            stego_path += ".wav"
            encode_audio(cover, current_payload, stego_path, key)

        elif layer_type == "text":

            stego_path += ".txt"

            with open(cover, "r", encoding="utf-8") as f:
                cover_text = f.read()

            stego_text = encode_text(cover_text, current_payload, key)

            with open(stego_path, "w", encoding="utf-8") as f:
                f.write(stego_text)

        else:
            raise ValueError("Unsupported media type")

        current_payload = stego_path

    return stego_path


def decode_nested(stego_file, output_folder, keys):

    os.makedirs(output_folder, exist_ok=True)

    current_file = stego_file

    for i, key in enumerate(keys):

        ext = os.path.splitext(current_file)[1].lower()

        if ext in [".png", ".jpg", ".jpeg"]:
            current_file = decode_image(current_file, output_folder, key)

        elif ext in [".mp4", ".avi"]:
            current_file = decode_video(current_file, output_folder, key)

        elif ext in [".wav"]:
            current_file = decode_audio(current_file, output_folder, key)

        elif ext in [".txt"]:

            with open(current_file, "r", encoding="utf-8") as f:
                stego_text = f.read()

            current_file = decode_text(stego_text, output_folder, key)

        else:
            raise ValueError("Unsupported stego file type")

        print(f"Layer {i+1} opened → {current_file}")

    return current_file