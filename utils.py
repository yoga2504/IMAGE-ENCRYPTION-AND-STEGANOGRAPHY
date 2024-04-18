from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
from utils import chaos_encrypt, lsb_steganography, chaos_decrypt, lsb_steganography_extract
import os
from PIL import Image

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    image = Image.open(request.files['image'])
    secret_image = Image.open(request.files['secret_image'])
    secret_image = secret_image.resize(image.size)
    if secret_image.mode == 'RGBA':
        secret_image = secret_image.convert('RGB')
    r = 3.9
    x0 = 0.5
    encrypted_secret_image = chaos_encrypt(secret_image, r, x0)
    stego_image = lsb_steganography(image, encrypted_secret_image)
    stego_image.save('static/stego_image.png')
    return send_file('static/stego_image.png', mimetype='image/png')

@app.route('/extract', methods=['POST'])
def extract_files():
    stego_image = Image.open(request.files['stego_image'])
    encrypted_secret_image = lsb_steganography_extract(stego_image)
    r = 3.9
    x0 = 0.5
    secret_image = chaos_decrypt(encrypted_secret_image, r, x0)
    secret_image.save('static/extracted_secret_image.png')
    return send_file('static/extracted_secret_image.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)