import argparse
import sys
import json

from core.nested_stego import encode_nested, decode_nested
from core.image_stego import encode_image, decode_image
from core.audio_stego import encode_audio, decode_audio
from core.video_stego import encode_video, decode_video
from core.text_stego import encode_text, decode_text


# --------------------------------------------------
# Encode single layer
# --------------------------------------------------

def encode(args):

    try:

        if args.type == "image":
            encode_image(args.cover, args.secret, args.output, args.key)

        elif args.type == "audio":
            encode_audio(args.cover, args.secret, args.output, args.key)

        elif args.type == "video":
            encode_video(args.cover, args.secret, args.output, args.key)

        elif args.type == "text":

            with open(args.cover, "r", encoding="utf-8") as f:
                cover_text = f.read()

            stego_text = encode_text(cover_text, args.secret, args.key)

            with open(args.output, "w", encoding="utf-8") as f:
                f.write(stego_text)

        else:
            raise ValueError("Unsupported media type")

        print("Encoding completed successfully.")

    except Exception as e:
        print("Encoding failed:", e)


# --------------------------------------------------
# Decode single layer
# --------------------------------------------------

def decode(args):

    try:

        if args.type == "image":
            decode_image(args.stego, args.output, args.key)

        elif args.type == "audio":
            decode_audio(args.stego, args.output, args.key)

        elif args.type == "video":
            decode_video(args.stego, args.output, args.key)

        elif args.type == "text":

            with open(args.stego, "r", encoding="utf-8") as f:
                stego_text = f.read()

            decode_text(stego_text, args.output, args.key)

        else:
            raise ValueError("Unsupported media type")

        print("Decoding completed successfully.")

    except Exception as e:
        print("Decoding failed:", e)


# --------------------------------------------------
# Nested Encode CLI
# --------------------------------------------------

def encode_nested_cli(args):

    with open(args.config, "r") as f:
        config = json.load(f)

    layers = config["layers"]

    result = encode_nested(
        args.secret,
        layers,
        args.output
    )

    print("Final stego file:", result)


# --------------------------------------------------
# Nested Decode CLI
# --------------------------------------------------

def decode_nested_cli(args):

    result = decode_nested(
        args.stego,
        args.output,
        args.keys
    )

    print("Final extracted file:", result)


# --------------------------------------------------
# Main CLI
# --------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Multimedia Steganography Tool"
    )

    subparsers = parser.add_subparsers(dest="command")

    # -----------------------
    # Encode command
    # -----------------------

    encode_parser = subparsers.add_parser("encode")

    encode_parser.add_argument(
        "type",
        choices=["image", "audio", "video", "text"],
        help="Type of cover media"
    )

    encode_parser.add_argument("cover", help="Cover file path")
    encode_parser.add_argument("secret", help="Secret file path")
    encode_parser.add_argument("output", help="Output stego file path")

    encode_parser.add_argument(
        "--key",
        help="Encryption key (optional)",
        default=None
    )

    encode_parser.set_defaults(func=encode)

    # -----------------------
    # Decode command
    # -----------------------

    decode_parser = subparsers.add_parser("decode")

    decode_parser.add_argument(
        "type",
        choices=["image", "audio", "video", "text"],
        help="Type of stego media"
    )

    decode_parser.add_argument("stego", help="Stego file path")

    decode_parser.add_argument(
        "output",
        help="Output folder for extracted file"
    )

    decode_parser.add_argument(
        "--key",
        help="Encryption key (optional)",
        default=None
    )

    decode_parser.set_defaults(func=decode)

    # -----------------------
    # Nested Encode
    # -----------------------

    encode_nested_parser = subparsers.add_parser(
        "encode-nested",
        help="Nested multilayer encoding"
    )

    encode_nested_parser.add_argument(
        "secret",
        help="Secret file to hide"
    )

    encode_nested_parser.add_argument(
        "config",
        help="JSON config file describing layers"
    )

    encode_nested_parser.add_argument(
        "output",
        help="Output folder"
    )

    encode_nested_parser.set_defaults(func=encode_nested_cli)

    # -----------------------
    # Nested Decode
    # -----------------------

    decode_nested_parser = subparsers.add_parser(
        "decode-nested",
        help="Decode nested steganography"
    )

    decode_nested_parser.add_argument(
        "stego",
        help="Outer stego file"
    )

    decode_nested_parser.add_argument(
        "output",
        help="Output folder"
    )

    decode_nested_parser.add_argument(
        "--keys",
        nargs="+",
        required=True,
        help="Keys for each layer"
    )

    decode_nested_parser.set_defaults(func=decode_nested_cli)

    # -----------------------
    # Execute command
    # -----------------------

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit()

    args.func(args)


# --------------------------------------------------

if __name__ == "__main__":
    main()