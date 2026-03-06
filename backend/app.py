from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import base64

from cryptography.fernet import Fernet
import stego_functions
import ai_detector
import smart_selector

app = Flask(__name__)
CORS(app)


# Function to convert user key to Fernet key
def generate_key(user_key):

    import hashlib

    key = hashlib.sha256(user_key.encode()).digest()

    return base64.urlsafe_b64encode(key)


@app.route("/encode-image", methods=["POST"])
def encode_image():

    message = request.form["message"]
    key = request.form["key"]

    file = request.files["image"]

    nparr = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Generate encryption key
    fernet_key = generate_key(key)
    cipher = Fernet(fernet_key)

    # Encrypt message
    encrypted_message = cipher.encrypt(message.encode()).decode()

    # Hide encrypted message
    encoded = stego_functions.encode_image(img, encrypted_message)

    _, buffer = cv2.imencode(".png", encoded)

    img_base64 = base64.b64encode(buffer).decode()

    return jsonify({
        "image": "data:image/png;base64," + img_base64
    })


@app.route("/decode-image", methods=["POST"])
def decode_image():

    key = request.form["key"]

    file = request.files["image"]

    nparr = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    encrypted_message = stego_functions.decode_image(img)

    try:

        fernet_key = generate_key(key)

        cipher = Fernet(fernet_key)

        decrypted_message = cipher.decrypt(encrypted_message.encode()).decode()

        return jsonify({"message": decrypted_message})

    except:

        return jsonify({"message": "Wrong key or corrupted message"})


@app.route("/detect", methods=["POST"])
def detect():

    file = request.files["image"]

    nparr = np.frombuffer(file.read(), np.uint8)

    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    probability = ai_detector.detect_steganography(img)

    return jsonify({"probability": probability})


@app.route("/smart-select", methods=["POST"])
def smart_select():

    file = request.files["image"]

    nparr = np.frombuffer(file.read(), np.uint8)

    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    result = smart_selector.analyze_image(img)

    return jsonify(result)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
