#!/usr/bin/python

import RPi.GPIO as GPIO
import sys, os, getopt 
from time import sleep
from subprocess import call

PIR_PIN = 11                    
debug = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)        # number by phisical pin 
GPIO.setup(PIR_PIN, GPIO.IN)    # Read output from PIR motion sensor

def turn_hdmi(channel):

    output = None

    if not debug:
        output = open(os.devnull, "w")

    if GPIO.input(channel):          # GPIO in state HIGH
        call(["/opt/vc/bin/tvservice", "--preferred"],stdout=output)
    else:                            # GPIO in state LOW
        call(["/opt/vc/bin/tvservice", "--off"],stdout=output)


def readPir():

    if debug:
        print "Set initial state of HDMI port based on PIR input."
    turn_hdmi(PIR_PIN)

    try:
        GPIO.add_event_detect(PIR_PIN, GPIO.BOTH, callback=turn_hdmi, bouncetime=200)

        while True:
            sleep(1e6)

    finally:
        GPIO.cleanup()
        if debug:
            print "\n Reseting GPIO. End of program.\n"


def helper():
    sys.exit('\nUsage: %s --pir-pin n [--debug]\n' % sys.argv[0])


if __name__ == "__main__":

    if os.geteuid() != 0:
        print "/nRoot access needed. Try sudo."
        helper()
    elif len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:],"vp:",["verbose","debug","pir-pin="])
        except getopt.GetoptError:
            helper()

        for opt, arg in opts:

            if opt in ["--debug","-v","--verbose"]:
                print "Running in debug mode."
                debug=True

            elif opt in ["-p","--pir-pin"]:
                PIR_PIN = arg

            else:
                helper()

    readPir()
