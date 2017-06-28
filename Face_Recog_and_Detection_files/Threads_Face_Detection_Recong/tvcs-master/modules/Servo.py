#!/usr/bin/python

import time

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import DynamicObjectV2
Obj = DynamicObjectV2.Class

# put your imports here

def init(self):
    # put your self.registerOutput here
    self.registerOutput("servo", Obj("moving", False))

def run (self):
    # put your init and global variables here
    moving = False

    # main loop
    while 1:
        # put your logic here
        # you can use: output, getInputs, message 
        facePos = self.getInputs().facePos
        if (facePos.x > 0): moving = True
        else: moving = False

        self.output("servo", Obj("moving", moving))

        # if you want to limit framerate, put it at the end
        time.sleep(1)