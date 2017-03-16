import xbox_read
import create
import time
from zelda import play
import RPi.GPIO as GPIO

#Inititalize Servo Setup
panPin = 12                     #pan motion for pi-cam
tiltPin = 16                    #tilt motion for pi-cam
kinectPin = 13                  #tilt motion for kinect

GPIO.setmode(GPIO.BCM)
GPIO.setup(panPin,GPIO.OUT)
GPIO.setup(tiltPin, GPIO.OUT)
GPIO.setup(kinectPin, GPIO.OUT)

pan= GPIO.PWM(panPin,60)
tilt = GPIO.PWM(tiltPin, 60)
kinect = GPIO.PWM(kinectPin, 70)

servos = [pan, tilt, kinect]
positions = [7.5, 7.5, 9.7]
mins = [2.5, 2.5, 2.5]
maxs = [12.5, 12.5, 22]

pan.start(7.5)
tilt.start(7.5)
kinect.start(9.7)

def changeAngle(servo, inc, vin=0):
        if vin ==1:
                if inc >= mins[servo] or inc <=maxs[servo]:
                        servos[servo].ChangeDutyCycle(inc)
                        positions[servo] =inc
        else:
                myP = positions[servo]
                newP = myP + inc
                if inc >= mins[servo] or inc <=maxs[servo]:
                        servos[servo].ChangeDutyCycle(newP)
                        positions[servo] = newP

createOn=0                      
speed=0                         #define translational speed variable
speedCnst=.3                    #divisor to convert analog input to usable speed variable
turnCnst=.01                    #divisor to convert analog input to usable turn variable
time0=0                         #variable to hold current time

for event in xbox_read.event_stream(deadzone=12000):
	#Initialize Robot
        if event.key=='start':
                print("starting...")
                if createOn==0:
                        r=create.Create('/dev/ttyUSB0')
                        createOn=1
	#Foward Movement
        if event.key=='RT':
                print (event.value)
                r.go(speedCnst*(event.value),0)
                speed=(speedCnst*(event.value))
                print ("speed:", speed)
	#Reverse Movement
        if event.key=='LT':
                print (event.value)
                r.go(-speedCnst*(event.value),0)
                speed=(-speedCnst*(event.value))
                print ("speed:", speed)
        #Turning Control      
        if event.key=='X1':
                if event.value>7000:
                        r.go(speed,(-event.value)*turnCnst)
                elif event.value<-7000:
                        r.go(speed,(-event.value)*turnCnst)
                else:
                        r.go(speed,0)
        #Play Zelda Theme Song        
        if event.key=='Y':
                if event.value==1:
                        play()
                print (event.value)
        #90 degree turn left(counterclockwise)      
        if event.key=='dl':
                if event.value==1:
                        print (event.value)
                        r.go(0,75)
                        r.waitAngle(90)
                        r.stop()
                if event.value==0:
                        print (event.value)
        #90 degree turn right(clockwise)              
        if event.key=='dr':
                if event.value==1:
                        print (event.value)
                        r.go(0,-75)
                        r.waitAngle(-90)
                        r.stop()
                if event.value==0:
                        print(event.value)
          
        if event.key=='A':
                if event.value==1:
                        print (event.value)
                        r.go(50)
                if event.value==0:
                        print (event.value)
                        r.stop()
                          
        if event.key=='B':
                print (event.value)
                r.stop()
                  
        if event.key=='guide':
                if event.value==1 and (time.time()-time0)<3.0:
                        print ("guide:1")
                        print("time:",time.time()-time0)
                        print("Entering Race Mode...")
                        speedCnst=2
                        turnCnst=.1
        if event.value==0:
                time0=time.time()
                print("time:",time0)
        if event.key=='back':
                if event.value==1 and (time.time()-time0)<3.0:
                        print ("back:1")
                        print("time:",time.time()-time0)
                        print("Entering Normal Mode...")
                        speedCnst=.3
                        turnCnst=.01
                if event.value==0:
                        time0=time.time()
                        print("time:",time0)

                        #Servo Code

        if event.key=='Y2':
                if event.value>7000:
                        changeAngle(2,0.5)
                        print ("Servo Go Upy")
                if event.value<-7000:
                        changeAngle(2, -0.5)
                        print ("Servo Go Downy")
        if event.key=='RB':
                if event.value==1:
                        changeAngle(2,0.5)
                        print ("Servo Go Upy")
        if event.key=='LB':
                if event.value==1:
                        changeAngle(2,-0.5)
                        print ("Servo Go Downy")
        #Position Servo to Center
        if event.key=='X':
                if event.value==1:
                        changeAngle(2, 9.7, vin=1)
                        #changeAngle(2,0.5)
                        print("Centering Servo")
        #Position Servo to High 
        if event.key=='du':
                if event.value==1:
                        changeAngle(2, 22, vin=1)
                        print("High Position")
        #Position Servo to Low
        if event.key=='dd':
                if event.value==1:
                        changeAngle(2, 2.5, vin=1)
                        print("Low Position")
                

