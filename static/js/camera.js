var videoElement = document.getElementById('videoElement');
var canvas = document.createElement('canvas');
var emotionElement = document.querySelector('h1'); // Select the h1 element
var interval = 1000; // Capture frame every 1 second
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
        if (videoElement) {
            videoElement.srcObject = stream;
            videoElement.play();
        }
        // Capture frames every 1 second and send to backend
        setInterval(function () {
            if (videoElement && canvas) {
                captureAndSendFrame();
            }
        }, interval);
    })
        .catch(function (err) {
        console.error("Error accessing webcam: ", err);
    });
}
else {
    console.error("getUserMedia not supported by this browser.");
}
function captureAndSendFrame() {
    if (!videoElement || !canvas)
        return;
    // Set canvas dimensions to video frame dimensions
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    var context = canvas.getContext('2d');
    if (context) {
        // Draw the current video frame onto the canvas
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        // Convert the canvas to a blob (JPEG format)
        canvas.toBlob(function (blob) {
            if (blob) {
                // Create a form data object to send the frame
                var formData = new FormData();
                formData.append('image', blob, 'frame.jpg');
                // Send the frame to the backend
                fetch('/process-frame', {
                    method: 'POST',
                    body: formData
                })
                    .then(function (response) { return response.json(); })
                    .then(function (data) {
                    console.log('Frame processed:', data);
                    if (data.emotion && data.score) {
                        // Update the h1 element with the detected emotion
                        if (emotionElement) {
                            emotionElement.textContent = "Detected Emotion: ".concat(data.emotion, ", Score: ").concat(data.score.toFixed(4));
                        }
                    }
                })
                    .catch(function (error) {
                    console.error('Error sending frame to backend:', error);
                });
            }
        }, 'image/jpeg');
    }
}
