import time
import sys

yesChoice = ['yes','y']
noChoice = ['no','n']

input = raw_input("Would you like to load Database? (y/n) ").lower()

if input in yesChoice:
    print "Loading Database."
    name ='Unknown'
    print(name)
elif input in noChoice:
    print "OK."
    exit 
else:
    print "Invalid input.\nExiting."
    exit
try:
    while True:
        input2 = raw_input("Would you like to search for people/detect faces? (y/n) ").lower()

        if input in yesChoice:
            print "Searching."
        elif input in noChoice:
            print "OK."
            exit 
        else:
            print "Invalid input.\nExiting."
            exit

## Exit, ctrl + c, Cleans up I/O's 
except KeyboardInterrupt:
    print "Closing..."
    time.sleep(0.5)
    sys.exit(0)


