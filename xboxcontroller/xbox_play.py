import sys
import subprocess
import xbox_read
import create
import time
from zelda import play
import RPi.GPIO as GPIO


f = open('xbox_control.rec', 'r')


#Inititalize Servo Setup
panPin = 12						#pan motion for pi-cam
tiltPin = 16					#tilt motion for pi-cam
kinectPin = 13					#tilt motion for kinect

GPIO.setmode(GPIO.BCM)
GPIO.setup(panPin,GPIO.OUT)
GPIO.setup(tiltPin, GPIO.OUT)
GPIO.setup(kinectPin, GPIO.OUT)



r=create.Create('/dev/ttyUSB0')

while(1):
	try:
		motion = f.readline()
		speed = float(f.readline())
		rotation = float(f.readline())
		waitTime = float(f.readline())
		
		print("Going ", motion, " (" + str(speed) + ',' + str(rotation) + ') waiting for' + str(waitTime))
		r.go(speed, rotation)
		
		time.sleep(waitTime)
	except (EOFError,ValueError): 
		r.stop()
		break
	
	
	
	
	