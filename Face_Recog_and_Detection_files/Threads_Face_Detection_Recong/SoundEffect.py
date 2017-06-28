########################################################
#this thread is a modified verstion of the one used by the
#Bohemian Raspbian team there origional code just checked to see if
#motors were moving and played a single sound.
#the new code checks if motors are moing and if the text to speak is quiet
# if these two things are met it will randly pick and play a sound effect
#from a large list the hope is that each time it moves the lamp will sound different
#but with a underlying theme
#
#moder: David O Mahony
#date: 06/03/2016
#team: embedded system design
#
######################################################
#!/usr/bin/python

import os
import subprocess
import signal
import time
import inspect
import random

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import IPCThread
IPCThread = IPCThread.Class

import DynamicObjectV2
Obj = DynamicObjectV2.Class

# put your vars here
path = str(os.path.realpath(__file__)).split("/")
path.pop() # remove last element i.e. this filename
strpath = ""
for element in path:
    strpath += element + "/"
strpath += "sounds/"

class Class (IPCThread):

    def __init__(self, name, API):
        IPCThread.__init__(self, name, API)

        self.registerOutput("audio", {"playing": False})

    def run(self):
        currentSound = None
        while 1:
            time.sleep(0.05)
            #servo = self.getInputs().servo
            servo = Obj("working", True)
            ttos = self.getInputs().ttos
            playing = False

            if not ttos.playing:

                if (servo.working): playing = True
            if (playing):
                if (currentSound and not self.isPlaying(currentSound)): currentSound = None
                if (not currentSound):
                        self.message ("here")
                        self.picksound()
            else:
                if (self.isPlaying(currentSound)):
                    self.kill(currentSound)
                    currentSound = None

            self.output("audio", {"playing": playing})

    def play (self, filename):
        proc = subprocess.Popen("mpg123 -q " + strpath + filename + "", stdout = subprocess.PIPE, shell = True, preexec_fn=os.setsid)
        wait.sleep(3)
        return proc

    def kill (self, proc):
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

    def isPlaying (self, proc):
        if (not proc):
            return False
        playing = (proc.poll() == None)
        return playing

    def picksound(self):
        #randis the sound witch will be played
        #rand will equal a rand value thatwill pick one of the sound files to be played
        rand=random.randrange(1, 29);
        if(rand==1):currentSound    = self.play("sound1.mp3")
        elif(rand==2):currentSound  = self.play("sound2.mp3")
        elif(rand==3):currentSound  = self.play("sound3.mp3")
        elif(rand==4):currentSound  = self.play("sound4.mp3")
        elif(rand==5):currentSound  = self.play("sound5.mp3")
        elif(rand==6):currentSound  = self.play("sound6.mp3")
        elif(rand==7):currentSound  = self.play("sound7.mp3")
        elif(rand==8):currentSound  = self.play("sound8.mp3")
        elif(rand==9):currentSound  = self.play("sound9.mp3")
        elif(rand==10):currentSound = self.play("sound10.mp3")
        elif(rand==11):currentSound = self.play("sound11.mp3")
        elif(rand==12):currentSound = self.play("sound12.mp3")
        elif(rand==13):currentSound = self.play("sound13.mp3")
        elif(rand==14):currentSound = self.play("sound14.mp3")
        elif(rand==15):currentSound = self.play("sound15.mp3")
        elif(rand==16):currentSound = self.play("sound16.mp3")
        elif(rand==17):currentSound = self.play("sound17.mp3")
        elif(rand==18):currentSound = self.play("sound18.mp3")
        elif(rand==19):currentSound = self.play("sound19.mp3")
        elif(rand==20):currentSound = self.play("sound20.mp3")
        elif(rand==21):currentSound = self.play("sound21.mp3")
        elif(rand==22):currentSound = self.play("sound22.mp3")
        elif(rand==23):currentSound = self.play("sound23.mp3")
        elif(rand==24):currentSound = self.play("sound24.mp3")
        elif(rand==25):currentSound = self.play("sound25.mp3")
        elif(rand==26):currentSound = self.play("sound26.mp3")
        elif(rand==27):currentSound = self.play("sound27.mp3")
        elif(rand==28):currentSound = self.play("sound28.mp3")
        elif(rand==29):currentSound = self.play("sound29.mp3")

