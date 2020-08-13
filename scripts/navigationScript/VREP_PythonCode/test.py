#!/usr/bin/python

# import the  bot module - this will include math, time, numpy (as np) and vrep python modules
from roverbot_lib import *

# SET SCENE PARAMETERS
sceneParameters = SceneParameters()

# SET ROBOT PARAMETERS
robotParameters = RobotParameters()
robotParameters.driveType = 'differential'	# specify if using differential (currently differential is only supported)

# MAIN SCRIPT
if __name__ == '__main__':

	# Wrap everything in a try except case that catches KeyboardInterrupts. 
	# In the exception catch code attempt to Stop the VREP Simulator so don't have to Stop it manually when pressing CTRL+C
	try:
		roverBotSim = VREP_RoverRobot('127.0.0.1', robotParameters, sceneParameters)
		roverBotSim.StartSimulator()

		while True:
			roverBotSim.SetTargetVelocities(0.1, 0)  # forward and rotational velocity
			roverBotSim.UpdateObjectPositions() # needs to be called once within main code loop

	except KeyboardInterrupt as e:
		# attempt to stop simulator so it restarts and don't have to manually press the Stop button in VREP 
		roverBotSim.StopSimulator()