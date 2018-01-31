#!/usr/bin/python

import RPi.GPIO as GPIO
import sys, os, getopt, time
from subprocess import call

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)        # number by phisical pin 
GPIO.setup(11, GPIO.IN)         # Read output from PIR motion sensor

def turn_hdmi(mode="on"):

    if mode == "off":
        call(["/opt/vc/bin/tvservice", "--off"])
        time.sleep(1)
    else:
        call(["/opt/vc/bin/tvservice", "--preferred"])
        time.sleep(30)     # keep monitor on for at least 30 seconds
    
    return mode

def readPir(debug = False):

#    f = open(os.devnull, 'w')  # redirect stdout to /dev/null
#    sys.stdout = f

    if debug:
        print "Starting with monitor ON."
    status = turn_hdmi("on")         # by default, turn on HDMI


    while True:
        i = GPIO.input(11)
        if i == 0:                 # When output from motion sensor is LOW
            if status == "on":   # if monitor is ON, turn it off
                if debug:
                    print "No intruders, monitor goes OFF."
                status = turn_hdmi("off")
        elif i == 1:               # When output from motion sensor is HIGH
            if status == "off":  # if monitor is OFF, switch it off
                if debug:
                    print "Intruder detected, turning monitor ON."
                status = turn_hdmi("on")
        time.sleep(0.5)

def helper():
    sys.exit('Usage: %s [--debug]' % sys.argv[0])

if __name__ == "__main__":

    if os.geteuid() != 0:
        print "Root access needed. Try sudo."
        helper()
    elif len(sys.argv) > 1:
        if sys.argv[1] in ["--debug","-v","--verbose"]:
            print "Run in debug mode"
            readPir(True)
        else:
            helper()
    else:
        readPir()

   

