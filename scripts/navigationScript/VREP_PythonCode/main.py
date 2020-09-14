#!/usr/bin/python
import time
import math
import numpy as np
import sys



import navigation, state
# change this depending on if Simulation or robot
SIMULATION = True

# libraries for simulation vs hardware
if SIMULATION:
    import roverbot_lib as rbot
else:
    import RPi.GPIO as GPIO
    # import mobility/sample collect files
    #import vision files

# load simulation 
if SIMULATION:
    # SET SCENE PARAMETERS
    sceneParameters = rbot.SceneParameters()

LED_GREEN = 0
LED_RED = 1
LED_YELLOW = 2
v = 0
w = 0
nav = navigation.Navigation()
state = state.State()
# MAIN SCRIPT    
if __name__ == '__main__':
    try:
        if SIMULATION:
            sim = rbot.VREP_RoverRobot('192.168.137.1', robotParameters, sceneParameters)
            sim.StartSimulator()
        else:
            ledSetup()
        while True:
            sim.UpdateObjectPositions()
            objects = sim.GetDetectedObjects()
            sampleCollected = sim.SampleCollected()
            state.updateState(objects, sampleCollected)
            v, w = nav.updateVelocities(state)

            sim.SetTargetVelocities(v, w) #don't copy this line
            if not SIMULATION:
                ledIndicator(nav.stateMode)


    except KeyboardInterrupt as e:
        sim.StopSimulator()

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