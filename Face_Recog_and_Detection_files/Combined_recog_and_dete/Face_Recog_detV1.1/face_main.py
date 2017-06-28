"""Raspberry Pi Face Recognition Treasure Box
Treasure Box Script
Copyright 2013 Tony DiCola 
"""
import cv2

import config
import face
import glob
import os
import sys
import select


def is_letter_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if select.select([sys.stdin,],[],[],0.0)[0]:
		input_char = sys.stdin.read(1)
		return input_char.lower() == letter.lower()
	return False

if __name__ == '__main__':
	# Load training data into model
	print 'Loading training data...'
	model = cv2.createEigenFaceRecognizer()
	model.load(config.TRAINING_FILE)
	print 'Training data loaded!'
	# Initialize camer and box.
	camera = config.get_camera()
	print 'Press Ctrl-C to quit.'
	print '/////////////////////'
	print 'Waiting for user (Press "o")'
	
	while True:
                if  is_letter_input('o'):
                        # Check if capture should be made.
                        # TODO: Check if button is pressed.
                        print 'Searching for face...'
                        # Check for the positive face and unlock if found.
                        image = camera.read()
                        # Convert image to grayscale.
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                        # Get coordinates of single face in captured image.
                        print 'img'
                        result = face.detect_single(image)
                        cv2.imshow("Frame", image)
                        if result is None:
                                print 'Could not detect a face!'
                                        
                                continue
                        x, y, w, h = result
                        # Crop and resize image to face.
                        crop = face.resize(face.crop(image, x, y, w, h))
                        # Test face against model.
                        label, confidence = model.predict(crop)
                        print 'Predicted {0} face with confidence {1}'.format(
                                'POSITIVE'
                                
                                if label == config.POSITIVE_LABEL
                                else 'NEGATIVE', confidence)
                        
                        if label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD:
                                print 'Recognized face!'
                                print '///////////////////////'
                        else:
                                print 'Did not recognize face!'
                                print '///////////////////////'
                        print 'Waiting for user 2 (Press "o")'
                        
                        
