const videoElement: HTMLVideoElement | null = document.getElementById('videoElement') as HTMLVideoElement;
const canvas: HTMLCanvasElement | null = document.createElement('canvas');
const interval = 1000;

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      if (videoElement) {
        videoElement.srcObject = stream;
        videoElement.play();
      }

      // Capture frames every 5 seconds and send to backend
      setInterval(() => {
        if (videoElement && canvas) {
          captureAndSendFrame();
        }
      }, interval);
    })
    .catch((err) => {
      console.error("Error accessing webcam: ", err);
    });
} else {
  console.error("getUserMedia not supported by this browser.");
}

function captureAndSendFrame() {
  if (!videoElement || !canvas) return;

  // Set canvas dimensions to video frame dimensions
  canvas.width = videoElement.videoWidth;
  canvas.height = videoElement.videoHeight;

  const context = canvas.getContext('2d');
  if (context) {
    // Draw the current video frame onto the canvas
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    // Convert the canvas to a blob (JPEG format)
    canvas.toBlob((blob) => {
      if (blob) {
        // Create a form data object to send the frame
        const formData = new FormData();
        formData.append('image', blob, 'frame.jpg');

        // Send the frame to the backend
        fetch('/process-frame', {
          method: 'POST',
          body: formData
        })
        .then((response) => response.json())
        .then((data) => {
          console.log('Frame sent successfully:', data);
        })
        .catch((error) => {
          console.error('Error sending frame to backend:', error);
        });
      }
    }, 'image/jpeg');
  }
}