#!/usr/bin/python

import RPi.GPIO as GPIO
import sys, os, getopt, time
from subprocess import call

PIR_PIN = 11
debug = False


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)        # number by phisical pin 
GPIO.setup(PIR_PIN, GPIO.IN)         # Read output from PIR motion sensor

def turn_hdmi(channel):

    if GPIO.input(channel):          # GPIO in state HIGH
        call(["/opt/vc/bin/tvservice", "--preferred"])
        if debug:
            print "Intruder detected, turning monitor ON."
    else:                       # GPIO in state LOW
        call(["/opt/vc/bin/tvservice", "--off"])
        if debug:
            print "No intruders, monitor goes OFF."


def readPir():

#    f = open(os.devnull, 'w')  # redirect stdout to /dev/null
#    sys.stdout = f

    if debug:
        print "Set initial state of HDMI port based on PIR input."
    #call(["/opt/vc/bin/tvservice", "--off"])
    turn_hdmi(PIR_PIN)

    try:
        GPIO.add_event_detect(PIR_PIN, GPIO.BOTH, callback=turn_hdmi, bouncetime=200)

        while True:
            time.sleep(1e6)

    finally:
        GPIO.cleanup()
        if debug:
            print "Reseting GPIO. End of program."


def helper():
    sys.exit('Usage: %s [--debug]' % sys.argv[0])

if __name__ == "__main__":

    if os.geteuid() != 0:
        print "Root access needed. Try sudo."
        helper()
    elif len(sys.argv) > 1:
        if sys.argv[1] in ["--debug","-v","--verbose"]:
            print "Run in debug mode"
            debug=True
        else:
            helper()
    
    readPir()

   

