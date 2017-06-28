#### import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

### initialise variables
resx = 200
resy = 200
fps = 30
facex= 0
facey= 0
facew= 0
faceh= 0

servo0= 0
servo1= 0
ulimit = 100
llimit = 0
step = 5

xaxismid = resx/2
yaxismid = resy/2
offset = 50
scaling = 2

### start timer
#start = time.time()
### stop timer and print to console
#    pass
#print(time.time() - start)
 
### initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (resx, resy)
camera.framerate = 30

### grab an image from the camera
#camera.capture(rawCapture, format="bgr")
rawCapture = PiRGBArray(camera, size=(resx, resy))

### allow the camera to warmup
time.sleep(0.1)

###Load a cascade file for detecting faces and eyes
face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_eye.xml') 


### main loop
while True:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            ### grab the raw NumPy array representing the image, then initialize the timestamp
            ### and occupied/unoccupied text
            image = frame.array

            ###Convert to grayscale
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)      
            ###Load a cascade file for detecting faces and eyes
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            eyes = eye_cascade.detectMultiScale(gray, 1.1, 5)
            
            ###Draw a rectangle around every found face
            for (x,y,w,h) in faces:
                facex = x
                facey = y
                facew = w
                faceh = h
                
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(image,(ex,ey),(ex+ew,ey+eh),(0,255,0),1)

            ###Save the result image
            #cv2.imwrite('dface.jpg',image)
            ### display the image on screen and wait for a keypress
            #cv2.namedWindow('image',cv2.WINDOW_NORMAL)
            #cv2.imshow("Image", image)
            
            #Resize Image
            height = image.shape[0]
            width = image.shape[0]
            resized = cv2.resize(image, (height*scaling, width*scaling))
            rx = facex*scaling
            ry = facey*scaling
            rw = facew*scaling
            rh = faceh*scaling

            ## find centre of face
            cface = [(facew/2+facex)*scaling, (faceh/2+facey)*scaling]
            print str(cface[0]) + "," + str(cface[1])

            #Add Text and graphics
            cv2.putText(resized,'Face(s) found = '+str(len(faces)),(1,30), cv2.FONT_ITALIC, 1, (0, 0, 255))
            cv2.line(resized,((xaxismid-(offset/scaling))*scaling,0),((xaxismid-(offset/scaling))*scaling,resy*scaling),(0,255,0),1)
            cv2.line(resized,((xaxismid+(offset/scaling))*scaling,0),((xaxismid+(offset/scaling))*scaling,resy*scaling),(0,255,0),1)
            cv2.line(resized,(0,(yaxismid-(offset/scaling))*scaling),(resx*scaling,(yaxismid-(offset/scaling))*scaling),(0,255,0),1)
            cv2.line(resized,(0,(yaxismid+(offset/scaling))*scaling),(resx*scaling,(yaxismid+(offset/scaling))*scaling),(0,255,0),1)

            ### determine desired position of servos for a for a detected face position

            ### no face detected
            if faces == ():
                servo0 = 50
                servo1 = 50

            ###face detected
            if faces != ():
                ### limit the range of the servo positions
                if cface[0] > (xaxismid+(offset/scaling))*scaling:
                        servo0 = servo0 - step
                if cface[0] < (xaxismid-(offset/scaling))*scaling:
                        servo0 = servo0 + step
                if cface[0] > (xaxismid+(offset/scaling))*scaling and cface[0] < (xaxismid-(offset/scaling))*scaling:
                        servo0 = servo0
                if cface[1] > (yaxismid+(offset/scaling))*scaling:
                        servo1 = servo1 - step
                if cface[1] < (yaxismid-(offset/scaling))*scaling:
                        servo1 = servo1 + step

                ### check if face is in center of cam, i.e do nothing
                if cface[1] < (yaxismid+(offset/scaling))*scaling and (yaxismid-(offset/scaling))*scaling:
                        servo1 = servo1

                ### check if face is not in center of cam, i.e move
                if servo0 <= llimit+ step:
                        servo0 = llimit 
                if servo1 <= llimit+ step:
                        servo1 = llimit
                if servo0 >= ulimit- step:
                        servo0 = ulimit
                if servo1 >= ulimit- step:
                        servo1 = ulimit

                ###Add text and graphics for face
                cv2.rectangle(resized,(rx,ry),(rx+rw,ry+rh),(0,0,255),1)
                cv2.line(resized,(cface[0],cface[1]),(xaxismid*scaling,yaxismid*scaling),(0,255,0),1)            
                cv2.putText(resized,'' +str(cface[0]),(rx+rh+1,ry+rw), cv2.FONT_ITALIC, 1, (0, 0, 255),1)
                cv2.putText(resized,',' +str(cface[1]),(rx+rh+60,ry+rw), cv2.FONT_ITALIC, 1, (0, 0, 255),1)
                cv2.putText(resized,'Position= '+str(cface[0]),(1,60), cv2.FONT_ITALIC, 1, (0, 0, 255))
                cv2.putText(resized,', '+str(cface[1]),(230,60), cv2.FONT_ITALIC, 1, (0, 0, 255))
                cv2.putText(resized,'Servo= '+str(servo0),(1,100), cv2.FONT_ITALIC, 1, (0, 0, 255))
                cv2.putText(resized,', '+str(servo1),(165,100), cv2.FONT_ITALIC, 1, (0, 0, 255))

            ### show the frame
            #cv2.imshow("Frame", image)
            cv2.imshow("Frame", resized)
            
            key = cv2.waitKey(1) & 0xFF
            
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
            
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                    break
                
cv2.destroyAllWindows()
