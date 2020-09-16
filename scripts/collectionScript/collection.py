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


    def Open_ROT(self):
        self.servoPWM.ChangeDutyCycle(7.5)
        self.servoPWM.ChangeDutyCycle(0)
        print("Open")
        time.sleep(1)

    def Close_ROT(self):
        self.servoPWM.ChangeDutyCycle(3.5)    
        self.servoPWM.ChangeDutyCycle(0)
        print("Close")
        time.sleep(1)

    def Release_Ball(self):
        self.servoPWM.ChangeDutyCycle(5)
        self.servoPWM.ChangeDutyCycle(0)
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