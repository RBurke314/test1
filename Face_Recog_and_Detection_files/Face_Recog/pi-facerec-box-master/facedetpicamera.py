# import the necessary packages
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

FRAME_W=400
FRAME_H=240
x1=0
y1=0
z1=0
Default_X=float(80)
Default_Y=float(48)
Default_Z=float(75)


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (400, 240)#faster processing set to 160, 120
camera.framerate = 40 #max frame rate of 90 frames per second
rawCapture = PiRGBArray(camera, size=(400, 240))#faster processing set to 160, 120
 
# allow the camera to warmup
time.sleep(0.1)
cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

while True:
        # capture frames from the camera
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                img = frame.array
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                face=0
                faces = cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, width, height) in faces:
                        face=1
                        cv2.rectangle(img, (x,y), (x+width, y+height), (0, 255,0), 2)
                        #get the center position of face
                        x1 = ((x+width)/2)
                        y1 = ((y+height)/2)
                        z1 = ((width+height)/2)
                
                if face == 1:
                        Position_x  = float(((FRAME_W/2)-x1))
                        Position_y  = float((FRAME_H/2)-y1)
                        Position_z  = float(z1)
                else:
                        Position_x  = (Default_X)
                        Position_y  = (Default_Y)
                        Position_z  = (Default_Z)                
    
                cv2.putText(img,'cam_pan='+ str(Position_x),(1,50), cv2.FONT_ITALIC, 0.5,(0,0,255))
                cv2.putText(img,'cam_tilt='+ str(Position_y),(1,100), cv2.FONT_ITALIC, 0.5,(0,0,255))
                cv2.putText(img,'cam_focus='+ str(Position_z),(1,150), cv2.FONT_ITALIC, 0.5,(0,0,255))
                
                # show the frame
                print('cam_pan='+ str(Position_x))
                print('cam_tilt='+ str(Position_y))
                print('cam_focus='+ str(Position_z))
                print "Found {0} faces!".format(len(faces))
                print"Found: %d" % (face) 
                
                cv2.imshow("Frame", img)
                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)
 
                # if the `q` key was pressed, break from the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
cv2.destroyAllWindows()
