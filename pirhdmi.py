#!/usr/bin/python

import RPi.GPIO as GPIO
import sys, os, getopt, time
from subprocess import call

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)        #number by phisical pin 
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor

def readPir(debug):
    status = "off"         # [FIXME] this should be guessed by system
    while True:
        i=GPIO.input(11)
        if i==0:                 #When output from motion sensor is LOW
            if status == "on":   #if monitor is ON, tunr it off
                if debug:
                    print "No intruders",i
                call(["/opt/vc/bin/tvservice", "--off"])
                time.sleep(1)
                status = "off"
        elif i==1:               #When output from motion sensor is HIGH
            if status == "off":  # if monitor is OFF, switch it off
                if debug:
                    print "Intruder detected",i
                call(["/opt/vc/bin/tvservice", "--preferred"])
                time.sleep(30)     # monitor on for at least 30 seconds
                status = "on"

def main(argv):
    debug = True
    readPir(debug)

if __name__ == "__main__":

    if os.geteuid() != 0:
        print "I need root access. Run with sudo."
    else:
        readPir(sys.argv[1:])

