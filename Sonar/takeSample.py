import RPi.GPIO as GPIO
import time
import statistics as stat

GPIO.setmode(GPIO.BCM)

def takeSamples(TRIG,ECHO):
    """
    given the pins for Trig and Echo, takeSamples returns the distance from the
    sensor to the first obstacle it sees. It takes 10 samples and then takes the
    median of those (my attempt to add some sort of averaging

    """
    
    #how many samples?
    samples = 40;
    #sampleArray
    sampleArray = []
    
    #Setup defined pins as input or output
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    
    for ii in range(1,samples):
        #set trig low and wait for electrons to settle
        GPIO.output(TRIG, False)
        #print "Waiting For Sensor To Settle"
        time.sleep(0.2)
    
        #Trigger pulse for 10us
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        pulse_start = time.time()
        pulse_end = time.time()
        
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
        
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()     
                
        #get pulse duration
        pulse_duration = pulse_end - pulse_start

        #get distance
        #constant speed of sound at sea level 343m/s divided by 2 (only want time it took to get there)
        #might want to consider doing some calibrations, but this is probably good enough
        distance = pulse_duration * 17150

        #round to make it pretty
        distance = round(distance, 2)#cm #  *0.393#to inches

        #add sample to array
        sampleArray = sampleArray + [distance]

        print('this is sample' ,ii, 'with distance', distance)

    distance = stat.median(sampleArray)
    #print to line
    #print( "Distance:",distance,"cm")
    GPIO.cleanup() #cleanup
    return distance

    
