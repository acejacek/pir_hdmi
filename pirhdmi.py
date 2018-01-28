#!/usr/bin/python

import RPi.GPIO as GPIO
import sys, getopt, time
from subprocess import call

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)        #number by phisical pin 
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
while True:
       i=GPIO.input(11)
       if i==0:                 #When output from motion sensor is LOW
             # print "No intruders",i
             call(["/opt/vc/bin/tvservice", "--off"])
             time.sleep(1)
       elif i==1:               #When output from motion sensor is HIGH
             # print "Intruder detected",i
             call(["/opt/vc/bin/tvservice", "--preferred"])
             time.sleep(30)     # monitor on for at least 30 seconds
