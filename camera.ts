const videoElement: HTMLVideoElement | null = document.getElementById('videoElement') as HTMLVideoElement;
const canvas: HTMLCanvasElement | null = document.createElement('canvas');
const emotionElement: HTMLElement | null = document.querySelector('h1');
const rectanglesContainer: HTMLElement | null = document.getElementById('rectangles-container');
const interval = 1000; // Capture frame every 1 second

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
      if (videoElement) {
        videoElement.srcObject = stream;
        videoElement.play();
      }

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
  
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
  
    const context = canvas.getContext('2d');
    if (context) {
      context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
  
      canvas.toBlob((blob) => {
        if (blob) {
          const formData = new FormData();
          formData.append('image', blob, 'frame.jpg');
  
          fetch('/process-frame', {
            method: 'POST',
            body: formData
          })
          .then((response) => response.json())
          .then((data) => {
            if (data.emotion && data.score && emotionElement) {
              emotionElement.textContent = `Detected Emotion: ${data.emotion}, Score: ${data.score.toFixed(4)}`;
            }
  
            if (data.faces && rectanglesContainer) {
              // Clear old rectangles and labels
              rectanglesContainer.innerHTML = '';
  
              // Draw new rectangles and labels
              data.faces.forEach((face: { x: number, y: number, width: number, height: number, emotion: string }) => {
                // Create the rectangle div
                const rect = document.createElement('div');
                rect.classList.add('face-rectangle');
                rect.style.left = `${face.x}px`;
                rect.style.top = `${face.y}px`;
                rect.style.width = `${face.width}px`;
                rect.style.height = `${face.height}px`;
  
                // Create a label div for the emotion
                const label = document.createElement('div');
                label.classList.add('face-label');
                label.textContent = face.emotion;
                label.style.left = `${face.x}px`;
                label.style.top = `${face.y - 20}px`;  // Position it above the rectangle
  
                // Append the rectangle and label to the container
                rectanglesContainer.appendChild(rect);
                rectanglesContainer.appendChild(label);
              });
            }
          })
          .catch((error) => {
            console.error('Error sending frame to backend:', error);
          });
        }
      }, 'image/jpeg');
    }
  }  