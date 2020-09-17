#====================================#
# EGB320
# Collection Script
# Group SLAVES: Group 13
# 2020 Semester 2
# Alan Yu
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
        self.servoPWM.start(3)
        self.currentState = 0 
        self.prevState = 0


    def sampleManage(self, navRockState):
        self.currentState = navRockState
        if self.currentState == self.prevState:
            pass
        else:
            if self.currentState == 0:
                pass
            elif self.currentState == 1:
                self.Open_ROT()
                self.prevState = self.currentState
            elif self.currentState == 2:
                self.Close_ROT()
            elif self.currentState == 3:
                self.Release_Ball()
            

    def Open_ROT(self):
        self.servoPWM.ChangeDutyCycle(7.5)
        print("Open")
        time.sleep(1)

    def Close_ROT(self):
        self.servoPWM.ChangeDutyCycle(3.5)    
        print("Close")
        time.sleep(1)

    def Release_Ball(self):
        self.servoPWM.ChangeDutyCycle(5)
        print("Releasing Ball")
        time.sleep(1)

    # def sample_uncovered(self):  # Start sample_retrival 110mm away
    #     SetAngle(90)
    #     time.sleep(2)
    #     SetAngle(0)

    # def sample_covered(self):  # Start sample_retrival 110mm away
    #     SetAngle(0)
    #     time.sleep(2)
    #     SetAngle(90)