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
            self.Open_ROT2()
        elif self.currentState == 2:
            print("close rot")
            self.Close_ROT2()
        elif self.currentState == 3:
            self.Lander2()
        self.prevState = self.currentState
        
    def Test_ROT(self):
        for x in range (5,25):
            self.servoPWM.ChangeDutyCycle(x/2)
            time.sleep(1)
            self.servoPWM.ChangeDutyCycle(0)
            print(x/2)
            time.sleep(2)
        
        
             

    def Open_ROT(self):
        self.servoPWM.ChangeDutyCycle(6.8)
        print("Open")
        time.sleep(1)
        self.servoPWM.ChangeDutyCycle(0)

    def Close_ROT(self):
        self.servoPWM.ChangeDutyCycle(3.2)    
        print("Close")
        time.sleep(1)
        self.servoPWM.ChangeDutyCycle(0)

    def Lander(self):
        self.servoPWM.ChangeDutyCycle(4.9)
        print("Releasing Ball")
        time.sleep(1)
        self.servoPWM.ChangeDutyCycle(0)


    def commandCentreCollectionControl(self,command):
        if command == "o":
            self.Open_ROT()
        elif command == "p":
            self.Close_ROT()
        elif command == "l":
            self.Lander()

    def Open_ROT2(self):
        timeElapsed = time.time() - self.stateTime
        print("I'm Open Rot")
        print(timeElapsed)
        if timeElapsed < 0.25:
            if self.count <1:
                self.servoPWM.ChangeDutyCycle(6.8)
                self.count+=1
                print("Open")
        elif 0.25 < timeElapsed < 2:
            if self.count <2:
                self.servoPWM.ChangeDutyCycle(0)
                self.count+=1
            
        else:
            pass
            print("I'm passing Open Rot")

    def Close_ROT2(self):
        timeElapsed = time.time() - self.stateTime
        print("I'm Close Rot")
        print(timeElapsed)
        if timeElapsed < 0.3:
            if self.count <1:
                self.servoPWM.ChangeDutyCycle(3.2)
                self.count+=1
                print("Close")
        elif 0.3 < timeElapsed < 2:
            if self.count <2:
                self.servoPWM.ChangeDutyCycle(0)
                self.count+=1
        else:
            pass
            print("I'm passing Close Rot")


    def Lander2(self):
        timeElapsed = time.time() - self.stateTime
        print("I'm Lander")
        print(timeElapsed)
        if timeElapsed < 0.3:
            if self.count <1:
                self.servoPWM.ChangeDutyCycle(4.9)
                self.count+=1
                print("Lander Angled Up")
        elif 0.3 < timeElapsed < 2:
            if self.count <2:
                self.servoPWM.ChangeDutyCycle(0)
                self.count+=1
        else:
            pass
            print("I'm passing Lander")
