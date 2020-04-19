#!/usr/bin/env python3


import RPi.GPIO as GPIO
import time
import simpleaudio as sa


# ---------- INTITALISE SETTINGS AND MISC OBJECTS ----------
#power pin
GPIO_ECHO = 17
GPIO_TRIGGER = 27

#door settings
door_wait = 0.5 # +1
closed_distance = 15

#audio settings
audfile1 = '/home/pi/zavri/data/zavri.wav'
waveobj1 = sa.WaveObject.from_wave_file(audfile1)
audfile2 = '/home/pi/zavri/data/excellent.wav'
waveobj2 = sa.WaveObject.from_wave_file(audfile2)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    # if distance > 2500:
    #     distance = 0
    # elif distance < 0:
    #     raise IOError
    
    return distance

# while 1:
#     try:
#         print(["OFF", "ON"][GPIO.input(pwr)])
#         time.sleep(1)
#     except KeyboardInterrupt:
#         print("Ending")
#         exit()

if __name__ == '__main__':
    isopen = False;
    counter = 0;
    try:
        while True:
            try:
                dist = distance()
                print ("Measured Distance = %.1f cm" % dist)
                
                if dist > closed_distance:
                    counter = counter + 1;

                #first after closing
                elif isopen == True and dist > closed_distance: 
                    isopen = False
                    counter = 0
                    playobj = waveobj2.play()
                    playobj.wait_done()
                    
                else:
                    counter = 0

                if dist > closed_distance and counter > 2: #the limit has been reached

                    #first time
                    if dist > closed_distance and isopen == False: 
                        isopen = True;
                        time.sleep(door_wait)
                    
                    #still open
                    elif dist > closed_distance and isopen == True: 
                        isopen = True;
                        playobj = waveobj1.play()
                        playobj.wait_done()
                    
                    

            except IOError:
                print("Sensor is not responding.")
            except ValueError:
                print("Invalid distance value recieved.")
            finally:
                time.sleep(1)

 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
