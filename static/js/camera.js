var videoElement = document.getElementById('videoElement');
var canvas = document.createElement('canvas');
var emotionElement = document.querySelector('h1');
var rectanglesContainer = document.getElementById('rectangles-container');
var interval = 1000; // Capture frame every 1 second
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
        if (videoElement) {
            videoElement.srcObject = stream;
            videoElement.play();
        }
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
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    var context = canvas.getContext('2d');
    if (context) {
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        canvas.toBlob(function (blob) {
            if (blob) {
                var formData = new FormData();
                formData.append('image', blob, 'frame.jpg');
                fetch('/process-frame', {
                    method: 'POST',
                    body: formData
                })
                    .then(function (response) { return response.json(); })
                    .then(function (data) {
                    if (data.emotion && data.score && emotionElement) {
                        emotionElement.textContent = "Detected Emotion: ".concat(data.emotion, ", Score: ").concat(data.score.toFixed(4));
                    }
                    if (data.faces && rectanglesContainer) {
                        // Clear old rectangles and labels
                        rectanglesContainer.innerHTML = '';
                        // Draw new rectangles and labels
                        data.faces.forEach(function (face) {
                            // Create the rectangle div
                            var rect = document.createElement('div');
                            rect.classList.add('face-rectangle');
                            rect.style.left = "".concat(face.x, "px");
                            rect.style.top = "".concat(face.y, "px");
                            rect.style.width = "".concat(face.width, "px");
                            rect.style.height = "".concat(face.height, "px");
                            // Create a label div for the emotion
                            var label = document.createElement('div');
                            label.classList.add('face-label');
                            label.textContent = face.emotion;
                            label.style.left = "".concat(face.x, "px");
                            label.style.top = "".concat(face.y - 20, "px"); // Position it above the rectangle
                            // Append the rectangle and label to the container
                            rectanglesContainer.appendChild(rect);
                            rectanglesContainer.appendChild(label);
                        });
                    }
                })
                    .catch(function (error) {
                    console.error('Error sending frame to backend:', error);
                });
            }
        }, 'image/jpeg');
    }
}
