import numpy as np
import cv2
import sys, os
from glob import glob

#setup cam variables
FRAME_W = 800;
FRAME_H = 480;
face_cascade1 = cv2.CascadeClassifier('face.xml')
face_cascade2 = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(1)

# sets video resolution
ret = video_capture.set(3,800)
ret = video_capture.set(4,480)

#setup position variables
Position_x = 0;
Position_y = 0;
Position_z = 0;
facecount=0;

#setup servo varables
stepsize = 5
servoposX=0;
servoposY=0;
servoposZ=0;
servo0 = 0
servo1 = 0
servo2 = 0
servomin=0
servomax=200    
def Tracking():
    x1=0;
    y1=0;
    w1=0;
    h1=0;
    x2=0;
    y2=0;
    w2=0;
    h2=0;
    #setup grid variables
    resH = 0
    resW = 0
    scaling = 1
    # Capture frame-by-frame
    facecount=0;
    ret, frame = video_capture.read()
    
    # Resize Image
    resH = frame.shape[0]
    resW = frame.shape[0]
    frame = cv2.resize(frame, (resH * scaling, resW * scaling))
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    # detect objects
    # detect objects
    frontfaces = face_cascade1.detectMultiScale(frame,1.3,5)
    sidefaces = face_cascade2.detectMultiScale(frame,1.3,5)
    for (x1, y1, w1, h1) in frontfaces:
        facecount=1;
        cv2.rectangle(frame, (x1, y1), (x1+w1, y1+h1), (255, 0, 255), 2)
    if facecount == 0:
        for (x2, y2, w2, h2) in sidefaces:
            facecount=1;
            cv2.rectangle(frame, (x2, y2), (x2+w2, y2+h2), (255, 0, 255), 2)

    # Get the center of the face
    x = ((((x1+x2)/2) + ((w1+w2)/2)) /2)
    y = ((((y1+y2)/2) + ((h1+h2)/2)) /2)
    z = ((((w1+w2)/2) + ((h1+h2)/2)) /2)
    # Correct relative to center of image
    Position_x  = float(((FRAME_W/2)-x)-80)
    Position_y  = float((FRAME_H/2)-y)
    Position_z  = float(z)
    
    cv2.putText(frame,'cam_pan='+ str(Position_x),(1,150), cv2.FONT_ITALIC, 0.5,(0,0,255))
    cv2.putText(frame,'cam_tilt='+ str(Position_y),(1,200), cv2.FONT_ITALIC, 0.5,(0,0,255))
    cv2.putText(frame,'cam_focus='+ str(Position_z),(1,250), cv2.FONT_ITALIC, 0.5,(0,0,255))
    cv2.putText(frame, 'Face(s) found = '+ str(facecount),(1,300), cv2.FONT_ITALIC, 0.5,(0,0,255))

    cv2.putText(frame,'Servo0='+ str(servo0),(1,350), cv2.FONT_ITALIC, 0.5,(0,0,255))
    cv2.putText(frame,'Servo1='+ str(servo1),(1,400), cv2.FONT_ITALIC, 0.5,(0,0,255))
    cv2.putText(frame,'Servo2='+ str(servo2),(1,450), cv2.FONT_ITALIC, 0.5,(0,0,255))
    
    #X axis line grid
    cv2.line(frame,((resH/2),0),(resH/2, resW),(255,255,255),1)
    cv2.line(frame,((resH/4),0),(resH/4, resW),(255,255,255),1)
    cv2.line(frame,((resH*3/4),0),((resH*3/4), resW),(255,255,255),1)
    #Y axis line grid
    cv2.line(frame,(0,(resW/2)),(resH, (resW/2)),(255,255,255),1)
    cv2.line(frame,(0,(resW/4)),(resH, (resW/4)),(255,255,255),1)
    cv2.line(frame,(0,(resW*3/4)),(resH, (resW*3/4)),(255,255,255),1)
    
    # Display the resulting frame
    cv2.imshow('Video', frame)
    return Position_x, Position_y, Position_z, facecount

def Moveing():
    global servo0, servo1, servo2
    ### no face detected return to home position 
    if facecount == 0:
        servo0 = 50
        servo1 = 50
        servo2 = 50

    ###face detected 
    if facecount != 0:
        ### limit the range of the servo positions
        servoposX = Position_x
        servoposY = Position_y
        servoposZ = Position_z 
        print ("servo posX=%d" %(servoposX))
        print ("servo posY=%d" %(servoposY))
        print ("servo posZ=%d" %(servoposZ))
        if servoposX < 240:
            if servo0 != servomin:
                servo0 = servo0 - stepsize            
        if servoposX > 240:
            if servo0 != servomax:
                servo0 = servo0 + stepsize

        if servoposY < 150:
            if servo1 != servomin:
                servo1 = servo1 - stepsize
        if servoposY > 150:
            if servo1 != servomax:
                servo1 = servo1 + stepsize

        if servoposZ < 60:
            if servo2 != servomin:
                servo2 = servo2 - stepsize
        if servoposZ > 60:
            if servo2 != servomax:
                servo2 = servo2 + stepsize

    return 
    
    
while(True):
    Position_x, Position_y, Position_z, facecount = Tracking()
    Moveing()
    #print ("Position X=%d" %(Position_x))
    #print ("Position Y=%d" %(Position_y))
    #print ("Position Z=%d" %(Position_z))
    #print ("face state=%d" %(facecount))
    # q key shuts program down 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
