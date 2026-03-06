from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import base64

import steganography_engine as stego

app = Flask(__name__)
CORS(app)


# ---------------- IMAGE ----------------

@app.route("/encode-image", methods=["POST"])
def encode_image():

    message = request.form["message"]
    key = request.form["key"]

    file = request.files["image"]

    nparr = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    encoded = stego.encode_image(img, message)

    _, buffer = cv2.imencode(".jpg", encoded)

    img_base64 = base64.b64encode(buffer).decode()

    return jsonify({
        "image": "data:image/jpeg;base64," + img_base64
    })


@app.route("/decode-image", methods=["POST"])
def decode_image():

    file = request.files["image"]

    nparr = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    message = stego.decode_image(img)

    return jsonify({"message": message})


# ---------------- AUDIO ----------------

@app.route("/encode-audio", methods=["POST"])
def encode_audio():

    message = request.form["message"]

    file = request.files["audio"]

    filename = "temp.wav"
    file.save(filename)

    output = stego.encode_audio(filename, message, "stego_audio.wav")

    return jsonify({"status": "audio encoded"})


@app.route("/decode-audio", methods=["POST"])
def decode_audio():

    file = request.files["audio"]

    filename = "temp.wav"
    file.save(filename)

    message = stego.decode_audio(filename)

    return jsonify({"message": message})


# ---------------- VIDEO ----------------

@app.route("/encode-video", methods=["POST"])
def encode_video():

    message = request.form["message"]

    file = request.files["video"]

    filename = "temp.mp4"
    file.save(filename)

    output = stego.encode_video(filename, message, "stego_video.mp4")

    return jsonify({"status": "video encoded"})


# ---------------- TEXT ----------------

@app.route("/encode-text", methods=["POST"])
def encode_text():

    message = request.form["message"]

    output = stego.encode_text(
        "Sample_cover_files/cover_text.txt",
        message,
        "stego_text.txt"
    )

    return jsonify({"status": "text encoded"})


if __name__ == "__main__":
    app.run(port=5000, debug=True)