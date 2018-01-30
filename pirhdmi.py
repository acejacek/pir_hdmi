#!/usr/bin/python

import RPi.GPIO as GPIO
import sys, os, getopt, time
from subprocess import call

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)        # number by phisical pin 
GPIO.setup(11, GPIO.IN)         # Read output from PIR motion sensor

def readPir(debug):
    status = "off"         # [FIXME] this should be guessed by system

    #f = open(os.devnull, 'w')  # redirect stdout to /dev/null
    #sys.stdout = f

    while True:
        i=GPIO.input(11)
        if i==0:                 # When output from motion sensor is LOW
            if status == "on":   # if monitor is ON, tunr it off
                if debug:
                    print "No intruders, monitor goes OFF."
                call(["/opt/vc/bin/tvservice", "--off"])
                time.sleep(1)
                status = "off"
        elif i==1:               # When output from motion sensor is HIGH
            if status == "off":  # if monitor is OFF, switch it off
                if debug:
                    print "Intruder detected, turning monitor ON."
                call(["/opt/vc/bin/tvservice", "--preferred"])
                time.sleep(30)     # keep monitor on for at least 30 seconds
                status = "on"

def helper():
    sys.exit('Usage: sudo %s [--debug]' % sys.argv[0])

def main(params):
    debug = False
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--debug","-v","--verbose"]:
            print "Run in debug mode"
            debug = True
        else:
            helper()
    
    readPir(debug)

if __name__ == "__main__":

    if os.geteuid() != 0:
        print "Root access needed."
        helper()
    else:
        main(sys.argv[1])

