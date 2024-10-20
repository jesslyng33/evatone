# IMPORTS
import asyncio
from hume import AsyncHumeClient
from hume.expression_measurement.stream import Config
from hume.expression_measurement.stream.socket_client import StreamConnectOptions
from hume.expression_measurement.stream.types import StreamFace
import cv2
import os
import sys

# CAMERA

cap = cv2.VideoCapture(0) # open connection to camera



# turn on camera until loop is broken
while True:
    
    ret, frame = cap.read() # capture frame by frame
    cv2.imshow('Camera Feed', frame) # display the frame
    cv2.imwrite(f'frame.jpg', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): # stop camera if q is pressed
        break

# release camera and close all windows
cap.release()
cv2.destroyAllWindows()