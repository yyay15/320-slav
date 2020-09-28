import numpy as np
import imutils
import math
import time
import cv2 
import PiCamera
import PiRGBArray

camera=PiCamera(resolution=(1640,922),framerate=15)
camera.iso=100
# Wait for the automatic gain control to settle
time.sleep(2)
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
#for the lines above ensure that the shutter speed and exposure speed are the same as they are related
g = camera.awb_gains
#g is camera gain that is adjusted for the current image taken then set the gain value for instead of being
#automatically adjusted through auto awb
camera.awb_mode = 'off'
camera.awb_gains = g
i=0
while True:
    rawCapture=PiRGBArray(camera)#take an image and store it as a RGB array
    time.sleep(0.1)
    camera.capture(rawCapture,format="bgr")#use the image we took previously 
    img=rawCapture.array#store it as img in a numpy array
    i+=1
    cv2.imshow("Image",img)
    cv22.waitKey(0)
    if i>=30:
        break