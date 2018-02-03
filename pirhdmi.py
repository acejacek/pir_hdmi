#!/usr/bin/python

import RPi.GPIO as GPIO
import sys, os, getopt 
from time import sleep
from subprocess import call

def turn_hdmi(channel):

    output = None

    if not debug:
        output = open(os.devnull, "w")

    if GPIO.input(channel):          # GPIO in state HIGH
        call(["/opt/vc/bin/tvservice", "--preferred"],stdout=output)
    else:                            # GPIO in state LOW
        call(["/opt/vc/bin/tvservice", "--off"],stdout=output)


def readPir(pir_pin,gpio_mode=GPIO.BOARD, debug = False):

    if gpio_mode == GPIO.BOARD:
        ports = [3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26,29,31,32,33,35,36,37,38,40]
    else:
        ports = [2,3,4,17,27,22,10,9,11,5,6,13,19,26,14,15,18,23,24,25,8,7,12,16,20,21]

    if debug:
        print "Board mode: " + str(gpio_mode)
        print "PIR pin:    " + str(pir_pin)

    try:
        GPIO.setwarnings(False)
        GPIO.setmode(gpio_mode) 
        
        if pir_pin in ports:
            if GPIO.gpio_function(pir_pin) == GPIO.IN:
                GPIO.setup(pir_pin, GPIO.IN)    # Read output from PIR motion sensor
        else:
            print "\nERROR: pin is not an valid input."
            helper()

        if debug:
            print "Set initial state of HDMI port based on PIR input."
        turn_hdmi(pir_pin)

        GPIO.add_event_detect(pir_pin, GPIO.BOTH, callback=turn_hdmi, bouncetime=200)

        while True:
            sleep(1e6)

    finally:
        GPIO.cleanup()
        if debug:
            print "\n Reseting GPIO. End of program.\n"


def helper():
    sys.exit('''\

Usage: %s --pir-pin n [--gpio-mode BCM] [--debug]

Options:

-p --pir-pin n   parameter "n" is pin number, where PIR sensor is connected

-m --gpio-mode   GPIO pin numbering mode. Valid options:
                    BOARD - (default) pin number referring to number on board 
                    BCM   - pin number corresponds to Broadcom SOC channel
                    
-v --debug       display debug information

    ''' % sys.argv[0])


if __name__ == "__main__":

    if os.geteuid() != 0:
        print "\nERROR: Root access needed. Try sudo."
        helper()

    try:
        opts, args = getopt.getopt(sys.argv[1:],"vp:m:",["verbose","debug","pir-pin=","gpio-mode="])

    except getopt.GetoptError:
        helper()

    debug = False
    gpio_mode = GPIO.BOARD
    pir_pin = ""

    for opt, arg in opts:

        if opt in ["--debug","-v","--verbose"]:
            print "Running in debug mode."
            debug = True

        elif opt in ["-p","--pir-pin"]:
            if arg.isdigit():
                pir_pin = int(arg)
            else:
                print "\nERROR: Invalid pin number."
                helper()
        elif opt in ["-m","--gpio-mode"]:
            if arg == "BCM":
                gpio_mode = GPIO.BCM
            elif arg not in ["BCM","BOARD"]:
                print "\nERROR: Unknown GPIO board mode."
                helper()
        else:
            helper()

    if pir_pin == "":
        print "\nERROR: undefined PIR pin."
        helper()

    readPir(pir_pin,gpio_mode,debug)
