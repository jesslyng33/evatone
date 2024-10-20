import requests
import time
import asyncio

async def main():
    # Step 1: Start inference job (POST /v0/batch/jobs)
    response = requests.post(
        "https://api.hume.ai/v0/batch/jobs",
        headers={
            "X-Hume-Api-Key": "4pI4JMESdAFcX7YWA28TP4Fk7GFr6Oiw2zVmh7AizVV8lhP5",
            "Content-Type": "application/json"
        },
        json={
            "urls": [
                "https://hume-tutorials.s3.amazonaws.com/faces.zip"
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
