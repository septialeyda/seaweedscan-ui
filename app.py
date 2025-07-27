import os
import requests
import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

API_URL = "https://4e5c633147f0.ngrok-free.app/"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Read image and send to Colab API
            img = cv2.imread(filepath)
            _, img_encoded = cv2.imencode('.jpg', img)
            response = requests.post(API_URL, files={"file": ("image.jpg", img_encoded.tobytes())})
            data = response.json()

            detections = list(zip(data.get("classes", []), data.get("detections", [])))

            return render_template('index.html', uploaded=True, image_url=filepath, detections=detections)

    return render_template('index.html', uploaded=False)

if __name__ == '__main__':
    app.run(debug=True)
