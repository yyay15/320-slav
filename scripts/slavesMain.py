#====================================#
# EGB320
# Main Script
# Group SLAVES: Group 13
# 2020 Semester 2
# Alan Yu
# 
#====================================#


#---------------#
# Preamble
#---------------#
# Import Python Library for main
import sys, time
import RPi.GPIO as GPIO
# Set Global Parameters 
LED_GREEN = 0
LED_RED = 1
LED_YELLOW = 2

# Local modules

from mobilityScript import mobilityScript
from navigationScript import navigation, state
from visionScript import vision

# from collectionScript import
# from visionScript import
print("loadingclass...")
# Initialise Functions and Classes
drive = mobilityScript.Mobility()
vision = vision.Vision()
# nav
nav = navigation.Navigation() 
state = state.State()
ledSetup() #nav


#---------------#
# MainScript
#---------------#
print("beforemain")
if __name__ == '__main__':
    # Load Objects or Simulation
    # print("beforeSimCheck...")

    # print("afterSimCheck...")
    
    # Launch command centre

    # Initialise States for All System
    v = 0
    w = 0


    # Try Loading And running
    try:
        print("beforeWhile...")

        while(1):
            print("""
            Please select Drive Mode
            a    Automatic
            m    Manual - Discrete (Enter Button)
            n    Manual - Continuous (Hold button)
            q    quit
            """)
            userSelect = input()
            if  userSelect == "a":
                # CHUCK THAT CHUNK HERE
                while True:
                    vision.UpdateObjectPositions()
                    objects = vision.GetDetectedObjects()
                    sampleCollected = vision.SampleCollected()
                    state.updateState(objects, sampleCollected)
                    v, w = nav.updateVelocities(state)
                    drive.SetTargetVelocities(v, w)
                
            elif userSelect == "m":
                drive.manualControl()
            elif userSelect == "n":
                drive.continuousControl()
            elif userSelect == "q":
                drive.gpioClean()
                break
            else:
                print("Unknown Command")
    # Clean up when closing        
    except KeyboardInterrupt:
        if not SIMULATION:
            drive.gpioClean()
            print("CleanergoVRMMM...")




#---------------#
# Function definitions
#---------------#

def ledIndicator(state):
    if (state == 1):
        GPIO.output(LED_RED, HIGH)
        GPIO.output(LED_YELLOW, LOW)
        GPIO.output(LED_GREEN, LOW)
    elif (state == 3 or state == 7):
        GPIO.output(LED_YELLOW, HIGH)
        GPIO.output(LED_GREEN, LOW)
        GPIO.output(LED_RED, LOW)
    elif (state == 5 or state == 6):
        GPIO.output(LED_GREEN, HIGH)
        GPIO.output(LED_RED, LOW)
        GPIO.output(LED_YELLOW, LOW)
    else:
        GPIO.output(LED_RED, LOW)
        GPIO.output(LED_YELLOW, LOW)
        GPIO.output(LED_GREEN, LOW)

def ledSetup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setup(LED_YELLOW, GPIO.OUT)
    GPIO.setup(LED_RED, GPIO.OUT) 