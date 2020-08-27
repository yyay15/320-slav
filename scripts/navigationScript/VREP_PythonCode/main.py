#!/usr/bin/python
import time
import math
import numpy as np
import sys


import navigation
# change this depending on if Simulation or robot
SIMULATION = True

# libraries for simulation vs hardware
if SIMULATION:
    import roverbot_lib as rbot
# else:
    # import mobility/sample collect files
    #import vision files

# load simulation 
if SIMULATION:
    # SET SCENE PARAMETERS
    sceneParameters = rbot.SceneParameters()

    # SET ROBOT PARAMETERS
    robotParameters = rbot.RobotParameters()
    robotParameters.driveType = 'differential'	# specify if using differential (currently differential is only supported)

v = 0
w = 0
nav = navigation.Navigation()
# MAIN SCRIPT    
if __name__ == '__main__':
    try:
        sim = rbot.VREP_RoverRobot('127.0.0.1', robotParameters, sceneParameters)
        sim.StartSimulator()
        while True:
            sim.UpdateObjectPositions()
            objects = sim.GetDetectedObjects()
            v, w = nav.updateVelocities()
            sim.SetTargetVelocities(v, w)


    except KeyboardInterrupt as e:
        sim.StopSimulator()

    