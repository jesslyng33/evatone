import requests
import time
import asyncio
import cv2
import boto3
from flask import Flask, send_from_directory
import os

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

capture_frames(1)

app = Flask(__name__)

@app.route('/uploads/<path:filename>')
def serve_file(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(debug=True)

async def main():
    cap = cv2.VideoCapture(0)
    
    # Step 1: Start inference job (POST /v0/batch/jobs)
    response = requests.post(
        "https://api.hume.ai/v0/batch/jobs",
        headers={
            "X-Hume-Api-Key": "4pI4JMESdAFcX7YWA28TP4Fk7GFr6Oiw2zVmh7AizVV8lhP5",
            "Content-Type": "application/json"
        },
        json={
            "urls": [
                "http://127.0.0.1:5000/uploads/frame_0.jpg"
            ],
            "notify": True,
            "models": {
                "face": {}
            },
            "transcription": {}
        },
    )

    job_id = response.json().get('job_id')
    if not job_id:
        print(f"Failed to create job: {response.text}")
        return

    print(f"Job created successfully. Job ID: {job_id}")

    # Step 2: Poll for job completion
    while True:
        response2 = requests.get(
            f"https://api.hume.ai/v0/batch/jobs/{job_id}/predictions",
            headers={
                "X-Hume-Api-Key": "4pI4JMESdAFcX7YWA28TP4Fk7GFr6Oiw2zVmh7AizVV8lhP5"
            },
        )

        # If the job is still in progress, wait and retry
        if response2.status_code == 400 and "Job is in progress." in response2.text:
            print("Job is still in progress. Retrying in 5 seconds...")
            time.sleep(5)  # Wait for 5 seconds before polling again
        elif response2.status_code == 200:
            # If the job is complete, print the predictions
            print("Job completed successfully!")
            print(response2.json())
            break
        else:
            # Handle other possible errors
            print(f"Error: {response2.status_code}, {response2.text}")
            break

if __name__ == "__main__":
    asyncio.run(main())