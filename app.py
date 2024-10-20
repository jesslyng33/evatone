from flask import Flask, render_template, request, jsonify
import os
import asyncio
from hume import AsyncHumeClient
from hume.expression_measurement.stream import Config
from hume.expression_measurement.stream.socket_client import StreamConnectOptions
from hume.expression_measurement.stream.types import StreamFace

app = Flask(__name__)

# Define the path where the images will be temporarily stored
UPLOAD_FOLDER = 'temp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to receive and process the frame from the frontend
@app.route('/process-frame', methods=['POST'])
def process_frame():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    image_file = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)
    
    # Asynchronously send the image to Hume API for emotion detection
    asyncio.run(process_with_hume(image_path))
    
    return jsonify({'status': 'success', 'message': 'Frame processed'})

async def process_with_hume(image_path):
    # Initialize the Hume client with the API key
    client = AsyncHumeClient(api_key="4pI4JMESdAFcX7YWA28TP4Fk7GFr6Oiw2zVmh7AizVV8lhP5")
    model_config = Config(face=StreamFace())
    stream_options = StreamConnectOptions(config=model_config)
    
    async with client.expression_measurement.stream.connect(options=stream_options) as socket:
        result = await socket.send_file(image_path)

        if result.face and result.face.predictions:
            # Extract the emotion with the highest score
            largest_score = result.face.predictions[0].emotions[0].score
            largest_emotion = result.face.predictions[0].emotions[0].name

            for i in range(1, len(result.face.predictions[0].emotions)):
                if result.face.predictions[0].emotions[i].score > largest_score:
                    largest_score = result.face.predictions[0].emotions[i].score
                    largest_emotion = result.face.predictions[0].emotions[i].name

            print(f"Emotion detected: {largest_emotion} (Score: {largest_score:.4f})")
        else:
            print("No predictions available.")

if __name__ == '__main__':
    app.run(debug=True)
