#====================================#
# EGB320
# Collection Script
# Group SLAVES: Group 13
# 2020 Semester 2
# Luis Serrano (Shout out Alan Yu)
#====================================#


#---------------#
# Preamble
#---------------#
# Import Python Library for collection
import RPi.GPIO as GPIO
import time

#---------------#
# Variables
#---------------#
# Pin configurations
servoPin = 17


# State Definition Key
# State 0 = pass
# State 1 = Open
# State 2 = Close
# State 3 = Slight Open
# State 4 = Hard Close
# State 5 = Drop Sample


################################################################
# Define Class System
###############################################################
class Collection:

    
    def __init__(self):
        # Set up GPIO Pins
        GPIO.setmode(GPIO.BCM)				
        GPIO.setup(servoPin, GPIO.OUT)			
        # Initialise PWM
        self.servoPWM = GPIO.PWM(servoPin, 50)
        # Initial Condition
        self.servoPWM.start(2.5)
        self.currentState = 0 
        self.prevState = 0
        self.stateTime = 0



    def sampleManage(self, navRockState):
        self.currentState = navRockState
        if self.currentState != self.prevState:
            self.stateTime = time.time()
            self.count = 0

        if self.currentState == 0:
            pass
        elif self.currentState == 1:
            self.Open_ROT()
        elif self.currentState == 2:
            self.Close_ROT()
        elif self.currentState == 3:
            self.Lander()
        elif self.currentState == 4: 
            self.Hard_Close_ROT()
            self.currentState = 2
        elif self.currentState == 5:
            self.Sample_Release()

        self.prevState = self.currentState
        
    def Test_ROT(self):
        for x in range (5,25):
            self.servoPWM.ChangeDutyCycle(x/2)
            time.sleep(1)
            self.servoPWM.ChangeDutyCycle(0)
            print(x/2)
            time.sleep(2)
        
    def commandCentreCollectionControl(self,command):
        if command == "o":
            self.Open_ROT2()
        elif command == "p":
            self.Hard_Close_ROT()
        elif command == "l":
            self.Lander()
      
             

    def Sample_Release(self):
        timeElapsed = time.time() - self.stateTime
        print("I'm Releasing Sample")
        print(timeElapsed)
        if timeElapsed < 1:
            if self.count <1:
                self.servoPWM.ChangeDutyCycle(8.0)
                self.count+=1
                print("Releasing")
        elif 1 < timeElapsed < 1.5:
            if self.count <2:
                self.servoPWM.ChangeDutyCycle(0)
                self.count+=1

    def Hard_Close_ROT(self):
        self.servoPWM.ChangeDutyCycle(3.3)    
        print("HARD CLOSE")
        time.sleep(1)
        self.servoPWM.ChangeDutyCycle(0)
    
    def Hard_Open_ROT(self):
        self.servoPWM.ChangeDutyCycle(7.3)    
        print("HARD OPEN")
        time.sleep(1)
        self.servoPWM.ChangeDutyCycle(0)

    def ROT_BOOT(self):
        self.servoPWM.ChangeDutyCycle(5.0)    
        print("Boot Seq - ROT")
        time.sleep(1)
        self.servoPWM.ChangeDutyCycle(0)



    def Open_ROT(self):
        timeElapsed = time.time() - self.stateTime
        print("I'm Open Rot")
        print("Open ROT ", timeElapsed)
        if timeElapsed < 1:
            if self.count <1:
                self.servoPWM.ChangeDutyCycle(7.2)
                self.count+=1
                print("Open")
        elif 1 < timeElapsed < 1.5:
            if self.count <2:
                self.servoPWM.ChangeDutyCycle(0)
                self.count+=1
            
        else:
            pass
            print("I'm passing Open Rot")

    def Close_ROT(self):
        timeElapsed = time.time() - self.stateTime
        print("I'm Close Rot")
        print("Close Rot ",timeElapsed)
        if timeElapsed < 1:
            if self.count <1:
                self.servoPWM.ChangeDutyCycle(3.0)
                self.count+=1
                print("Close")
        elif 1 < timeElapsed < 1.5:
            if self.count <2:
                self.servoPWM.ChangeDutyCycle(0)
                self.count+=1
        else:
            pass
            print("I'm passing Close Rot")


    def Lander(self):
        timeElapsed = time.time() - self.stateTime
        print("I'm Lander")
        print(timeElapsed)
        if timeElapsed < 1:
            if self.count <1:
                self.servoPWM.ChangeDutyCycle(5.2)
                self.count+=1
                print("Lander Angled Up")
        elif 1 < timeElapsed < 1.5:
            if self.count <2:
                self.servoPWM.ChangeDutyCycle(0)
                self.count+=1
        else:
            pass
            print("I'm passing Lander")
