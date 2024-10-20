import asyncio
from hume import AsyncHumeClient
from hume.expression_measurement.stream import Config
from hume.expression_measurement.stream.socket_client import StreamConnectOptions
from hume.expression_measurement.stream.types import StreamFace
import cv2
import os
import sys

def capture_frames(name, video_source=0):
    cap = cv2.VideoCapture(video_source)
    ret, frame = cap.read()
    cv2.imshow('Camera Feed', frame)
    
    if ret:  # Ensure the frame was captured successfully
        # Save the frame as a file (e.g., frame_1.jpg, frame_2.jpg, etc.)
        cv2.imwrite(f'frame_{name}.jpg', frame)

    cap.release()  # Release the camera

async def main():
    
    # Get root folder
    root_folder = os.path.abspath(os.path.join('..'))
    if root_folder not in sys.path:
        sys.path.append(root_folder)
        
    # Initialize the Hume client
    client = AsyncHumeClient(api_key="4pI4JMESdAFcX7YWA28TP4Fk7GFr6Oiw2zVmh7AizVV8lhP5")
    model_config = Config(face=StreamFace())
    stream_options = StreamConnectOptions(config=model_config)
        
    while True:
        cap = cv2.VideoCapture(0)
        _, frame = cap.read() # capture frame by frame
        cv2.imshow('Camera Feed', frame) # display the frame

        for i in range(20):
            capture_frames(i)
            file_path = os.path.join(root_folder, f'calhacks\\frame_{i}.jpg')

            async with client.expression_measurement.stream.connect(options=stream_options) as socket:
                result = await socket.send_file(file_path)

                if result.face and result.face.predictions:
                    largest_score = result.face.predictions[0].emotions[0].score
                    largest_emotion = result.face.predictions[0].emotions[0].name

                    # Find the largest emotion
                    for j in range(1, len(result.face.predictions[0].emotions)):
                        if result.face.predictions[0].emotions[j].score > largest_score:
                            largest_score = result.face.predictions[0].emotions[j].score
                            largest_emotion = result.face.predictions[0].emotions[j].name

                    print(f"Frame {i}: {largest_emotion} (Score: {largest_score:.4f})")
                else:
                    print(f"Frame {i}: No predictions available.")

if __name__ == "__main__":
    asyncio.run(main())