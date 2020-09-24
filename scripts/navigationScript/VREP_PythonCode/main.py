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
    # SET ROBOT PARAMETERS
    robotParameters = rbot.RobotParameters()
    robotParameters.driveType = 'differential'	# specify if using differential (currently differential is only supported)
    # Drive Parameters
    robotParameters.minimumLinearSpeed = 0.0  	# minimum speed at which your robot can move forward in m/s
    robotParameters.maximumLinearSpeed = 0.25 	# maximum speed at which your robot can move forward in m/s
    robotParameters.driveSystemQuality = 1		# specifies how good your drive system is from 0 to 1 (with 1 being able to drive in a perfectly straight line when a told to do so)

    # Camera Parameters
    robotParameters.cameraOrientation = 'landscape' # specifies the orientation of the camera, either landscape or portrait
    robotParameters.cameraDistanceFromRobotCenter = 0.1 # distance between the camera and the center of the robot in the direction of the kicker/dribbler in metres
    robotParameters.cameraHeightFromFloor = 0.15 # height of the camera relative to the floor in metres
    robotParameters.cameraTilt = 0.35 # tilt of the camera in radians

    # Vision Processing Parameters
    robotParameters.maxBallDetectionDistance = 1 # the maximum distance away that you can detect the ball in metres
    robotParameters.maxLanderDetectionDistance = 2.5 # the maximum distance away that you can detect the goals in metres
    robotParameters.maxObstacleDetectionDistance = 1.5 # the maximum distance away that you can detect the obstacles in metres

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
            #172.19.44.254
            sim = rbot.VREP_RoverRobot('127.0.0.1', robotParameters, sceneParameters)
            #sim = rbot.VREP_RoverRobot('172.19.44.254', robotParameters, sceneParameters)
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

