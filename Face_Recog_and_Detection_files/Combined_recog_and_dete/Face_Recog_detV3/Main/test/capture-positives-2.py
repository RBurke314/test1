"""Raspberry Pi Face Recognition Treasure Box
Positive Image Capture Script
Copyright 2013 Tony DiCola 

Run this script to capture positive images for training the face recognizer.
"""
import glob
import os
import sys
import select
import time
import cv2
import io
import picamera
import numpy as np
#import config
#import face
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2







# Prefix for positive training image filenames.
POSITIVE_FILE_PREFIX = 'subject'
# if too many false negatives (undetected faces).
POSITIVE_THRESHOLD = 3000.0

# File to save and load face recognizer model.
TRAINING_FILE = 'training.xml'

# Directories which contain the positive and negative training image data.
POSITIVE_DIR = './training/positive'
NEGATIVE_DIR = './training/negative'

# Value for positive and negative labels passed to face recognition model.
# Can be any integer values, but must be unique from each other.
# You shouldn't have to change these values.
POSITIVE_LABEL = 1
NEGATIVE_LABEL = 2

# Size (in pixels) to resize images for training and prediction.
# Don't change this unless you also change the size of the training images.
FACE_WIDTH  = (92/3)
FACE_HEIGHT = (112/3)

# Face detection cascade classifier configuration.
# You don't need to modify this unless you know what you're doing.
# See: http://docs.opencv.org/modules/objdetect/doc/cascade_classification.html
HAAR_FACES         = 'haarcascade_frontalface_default.xml'
HAAR_SCALE_FACTOR  = 1.3
HAAR_MIN_NEIGHBORS = 4
HAAR_MIN_SIZE      = (30, 30)

# Filename to use when saving the most recently captured image for debugging.
DEBUG_IMAGE = 'capture.pgm'

def get_camera():	
	# Camera to use for capturing images.
	# Use this code for capturing from the Pi camera:
	
	return OpenCVCapture()
	# Use this code for capturing from a webcam:
	# import webcam
	# return webcam.OpenCVCapture(device_id=0)

def is_letter_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if select.select([sys.stdin,],[],[],0.0)[0]:
		input_char = sys.stdin.read(1)
		return input_char.lower() == letter.lower()
	return False
def detect_single(image):
	"""Return bounds (x, y, width, height) of detected face in grayscale image.
	   If no face or more than one face are detected, None is returned.
	"""
	faces = haar_faces.detectMultiScale(image, 
				scaleFactor=HAAR_SCALE_FACTOR, 
				minNeighbors=HAAR_MIN_NEIGHBORS, 
				minSize=HAAR_MIN_SIZE, 
				flags=cv2.CASCADE_SCALE_IMAGE)
	if len(faces) != 1:
		return None
	return faces[0]

def crop(image, x, y, w, h):
	"""Crop box defined by x, y (upper left corner) and w, h (width and height)
	to an image with the same aspect ratio as the face training data.  Might
	return a smaller crop if the box is near the edge of the image.
	"""
	crop_height = int((FACE_HEIGHT / float(FACE_WIDTH)) * w)
	midy = y + h/2
	y1 = max(0, midy-crop_height/2)
	y2 = min(image.shape[0]-1, midy+crop_height/2)
	return image[y1:y2, x:x+w]

def resize(image):
	"""Resize a face image to the proper size for training and detection.
	"""
	return cv2.resize(image, 
					  (FACE_WIDTH, FACE_HEIGHT), 
					  interpolation=cv2.INTER_LANCZOS4)

class OpenCVCapture(object):
	def read(self):
		"""Read a single frame from the camera and return the data as an OpenCV
		image (which is a numpy array).
		"""
		# This code is based on the picamera example at:
		# http://picamera.readthedocs.org/en/release-1.0/recipes1.html#capturing-to-an-opencv-object
		# Capture a frame from the camera.
		data = io.BytesIO()
		with picamera.PiCamera() as camera:
			camera.capture(data, format='jpeg')
		data = np.fromstring(data.getvalue(), dtype=np.uint8)
		# Decode the image data and return an OpenCV image.
		image = cv2.imdecode(data, 1)
		# Save captured image for debugging.
		cv2.imwrite(DEBUG_IMAGE, image)
		
		# Return the captured image data.
		return image



if __name__ == '__main__':
	camera = get_camera()
	haar_faces = cv2.CascadeClassifier(HAAR_FACES)
	
	# Create the directory for positive training images if it doesn't exist.
	if not os.path.exists(POSITIVE_DIR):
		os.makedirs(POSITIVE_DIR)
	# Find the largest ID of existing positive images.
	# Start new images after this ID value.
	files = sorted(glob.glob(os.path.join(POSITIVE_DIR, 
		POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].pgm')))
	count = 0
	if len(files) > 0:
		# Grab the count from the last filename.
		count = int(files[-1][-7:-4])+1
	print ('Capturing positive training images.')
	print ('Press button or type c (and press enter) to capture an image.')
	print ('Press Ctrl-C to quit.')
	while True:
                
                #prompt = input('Press 1 to take pic')
		#x = int(prompt)
		#print ('Capturing image')#prompt = input('press 1 to take pic')
                #x = int(prompt)
		# Check if button was pressed or 'c' was received, then capture image.
		#print ('Capturing image...')
		prompt = input('Press 1 to take pic')
		x = int(prompt)
		print('Capturing image')
		image = camera.read()
		time.sleep(0.1)
		# Convert image to grayscale.
		image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		# Get coordinates of single face in captured image.
		result = detect_single(image)
		img = cv2.resize(image,(500,500), interpolation = cv2.INTER_CUBIC)
		cv2.imshow("hi",img)
		cv2.waitKey(200)
		
		
		if result is None:
			print ('Could not detect single face!')
			continue
		x, y, w, h = result
		# Crop image as close as possible to desired face aspect ratio.
		# Might be smaller if face is near edge of image.
		crop = crop(image, x, y, w, h)
		# Save image to file.
		filename = os.path.join(POSITIVE_DIR, POSITIVE_FILE_PREFIX + '%03d.pgm' % count)
		cv2.imwrite(filename, crop)
		print ('Found face and wrote training image'), filename
		count += 1

