# IMPORTS
import cv2

# CAMERA

cap = cv2.VideoCapture(0) # open connection to camera

# pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# turn on camera until loop is broken
while True:
    ret, frame = cap.read() # capture frame by frame
    cv2.imshow('Camera Feed', frame) # display the frame
    
    # convert the frame to grayscale (needed for face detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # draw a rectangle around each detected face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # display the frame with rectangles around faces
    cv2.imshow('Camera Feed', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): # stop camera if q is pressed
        break

# release camera and close all windows
cap.release()
cv2.destroyAllWindows()