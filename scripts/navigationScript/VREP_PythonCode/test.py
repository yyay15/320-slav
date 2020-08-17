#!/usr/bin/python

# import the  bot module - this will include math, time, numpy (as np) and vrep python modules
from roverbot_lib import *
import readchar

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
		v = 0
		w = 0
		while True:
			roverBotSim.UpdateObjectPositions() # needs to be called once within main code loop
			samplesRB, landerRB, obstaclesRB, rocksRB = roverBotSim.GetDetectedObjects()
			if rocksRB != None:
				rangeObs = rocksRB[0][0]
				bearingObs = rocksRB[0][1]
				if rangeObs <= 0.5:
					roverBotSim.SetTargetVelocities(0, 0)
				else:
					roverBotSim.SetTargetVelocities(rangeObs, bearingObs)
			else:
				roverBotSim.SetTargetVelocities(0, 0.1)
			# keyboard = readchar.readchar()
			# if keyboard == 'w':
			# 	v += 0.05
			# 	print(v)
			# if keyboard == 'a': 
			# 	w += 0.1
			# 	print(w)
			# if keyboard == 'd':
			# 	w -= 0.1
			# 	print(w)
			# if keyboard == 'q':
			# 	v = 0
			# 	w = 0

			#roverBotSim.SetTargetVelocities(0.1, 0)  # forward and rotational velocity

			# print("obstaclesRB: ", obstaclesRB)
			# print("samplesRB: ", samplesRB)
			# print("rocksRB: ", rocksRB)

	except KeyboardInterrupt as e:
		# attempt to stop simulator so it restarts and don't have to manually press the Stop button in VREP 
		roverBotSim.StopSimulator()