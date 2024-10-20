from flask import Flask, render_template, request, jsonify
import os
import cv2
import asyncio
from hume import AsyncHumeClient
from hume.expression_measurement.stream import Config
from hume.expression_measurement.stream.socket_client import StreamConnectOptions
from hume.expression_measurement.stream.types import StreamFace

app = Flask(__name__)

UPLOAD_FOLDER = 'temp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-frame', methods=['POST'])
def process_frame():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    image_file = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)

    image = cv2.imread(image_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    
    largest_emotion, largest_score = asyncio.run(process_with_hume(image_path))

    face_data = []  # Prepare list to store face info
    for (x, y, w, h) in faces:
        # Include coordinates and the emotion in the data sent back
        face_data.append({
            'x': int(x), 
            'y': int(y), 
            'width': int(w), 
            'height': int(h),
            'emotion': largest_emotion
        })

    return jsonify({
        'status': 'success',
        'message': 'Frame processed',
        'emotion': largest_emotion,  # Max emotion in frame
        'score': largest_score,
        'faces': face_data  # Send back coordinates and emotions for each face
    })

async def process_with_hume(image_path):
    client = AsyncHumeClient(api_key="4pI4JMESdAFcX7YWA28TP4Fk7GFr6Oiw2zVmh7AizVV8lhP5")
    model_config = Config(face=StreamFace())
    stream_options = StreamConnectOptions(config=model_config)

    async with client.expression_measurement.stream.connect(options=stream_options) as socket:
        result = await socket.send_file(image_path)

        if result.face and result.face.predictions:
            largest_score = result.face.predictions[0].emotions[0].score
            largest_emotion = result.face.predictions[0].emotions[0].name

            for i in range(1, len(result.face.predictions[0].emotions)):
                if result.face.predictions[0].emotions[i].score > largest_score:
                    largest_score = result.face.predictions[0].emotions[i].score
                    largest_emotion = result.face.predictions[0].emotions[i].name

            return largest_emotion, largest_score
        else:
            return None, 0.0

if __name__ == '__main__':
    app.run(debug=True)