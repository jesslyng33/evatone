import asyncio
from hume import AsyncHumeClient
from hume.expression_measurement.stream import Config
from hume.expression_measurement.stream.socket_client import StreamConnectOptions
from hume.expression_measurement.stream.types import StreamFace
import cv2
import os
import sys
import base64

def capture_frames(frames, video_source=0):
    cap = cv2.VideoCapture(video_source)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame as a file (e.g., frame_1.jpg, frame_2.jpg, etc.)
        cv2.imwrite(f'frame_{frame_count}.jpg', frame)
        frame_count += 1

        # Exit after capturing 10 frames, for example
        if frame_count >= frames:
            break

    cap.release()
    cv2.destroyAllWindows()

async def main():
    capture_frames(1)
    
    # get root folder
    root_folder = os.path.abspath(os.path.join('..'))
    if root_folder not in sys.path:
        sys.path.append(root_folder)

    file_path = os.path.join(root_folder, 'calhacks\\frame_0.jpg')
    
    client = AsyncHumeClient(api_key="4pI4JMESdAFcX7YWA28TP4Fk7GFr6Oiw2zVmh7AizVV8lhP5")
    model_config = Config(face=StreamFace())
    stream_options = StreamConnectOptions(config=model_config)
    async with client.expression_measurement.stream.connect(options=stream_options) as socket:
        result = await socket.send_file(file_path)
        print(result)

if __name__ == "__main__":
    asyncio.run(main())

