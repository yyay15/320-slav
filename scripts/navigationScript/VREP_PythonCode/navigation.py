import time
import numpy as np
from math import * 
#import matplotlib.pyplot as plt

# STATES
SEARCH_SAMPLE = 1
SEARCH_ROCK = 2
NAV_SAMPLE = 3
NAV_ROCK = 4
SEARCH_LANDER = 5
NAV_LANDER = 6
ACQUIRE_SAMPLE = 7
UP_LANDER = 8
FLIP_ROCK = 9
HOLE_ALIGN = 10
SAMPLE_DROP = 11

#ROT CONSTANTS
# State 0 = pass
# State 1 = Open
# State 2 = Close
# State 3 = Slight Open
PASS_STATE = 0
OPEN = 1
CLOSE = 2
SLIGH_OPEN = 3

# DISTANCE/TIME VARIABLES
ROT_DISTANCE = 0.21 #collect distance 
FLIP_DISTANCE = 0.1
FULL_ROTATION = 15
ROT_ACQUIRE_SAMPLE = 1
DRIVE_OFF_TIME = 6
LANDER_SWITCH_RANGE = 0.1

# OBSTACLE AVOIDANCE GAINS 
KV_ATTRACT = 0.5 #0.5
KW_ATTRACT = 1.3    #1.5 #0.8
KV_REPULSE = 0.3
KW_REPULSE = 4

class Navigation:
    def __init__(self):
        self.stateMode = 5   # intial start state
        self.modeStartTime = time.time() # timer for each state
        self.turnDir = 1                 # turn clockwise or anticlockwise
        self.rock_obstacle = True        # check if rocks should be avoided
        self.rotState = CLOSE            # state for sample collection
        self.isBlind = False
        self.centering = False
        self.commandnav = False
        self.numSampleCollected = 0
        
    
    def currentState(self, stateNum):
        switchState = {
            1: self.searchSample,
            2: self.searchRock,
            3: self.navSample, 
            4: self.navRock, 
            5: self.searchLander,
            6: self.navLander,
            7: self.acquireSample,
            8: self.driveUpLander,
            9: self.flipRock,
            10: self.holeAlign,
            11: self.dropSample
        }
        return switchState.get(stateNum, self.searchSample)

    # calls relevant state function and returns target velocities
    def updateVelocities(self, state):
        v, w = self.currentState(self.stateMode)(state)
        return v, w

    # robot spins, moves forward, spins again
    def searchAll(self, state):
        # search both
        if (not self.isEmpty(state.sampleRB) or not self.isEmpty(state.rocksRB)):
            v, w = 0, 0
            # if both visible got to closest
            if not self.isEmpty(state.sampleRB) and not self.isEmpty(state.rocksRB):
                if state.sampleRB[0][0] < state.rocksRB[0][0]:
                    self.modeStartTime = time.time()
                    self.stateMode = NAV_SAMPLE
                else:
                    self.modeStartTime = time.time()
                    self.stateMode = NAV_ROCK
            # only sample visible
            if (not self.isEmpty(state.sampleRB)):
                self.modeStartTime = time.time()
                self.stateMode = NAV_SAMPLE
            # only rock visible
            else:
                self.modeStartTime = time.time()
                self.stateMode = NAV_ROCK
        elif(time.time() - self.modeStartTime >= FULL_ROTATION):
            print("moving around")
            v, w = self.navigate([0.2, 0], state)
            if (time.time() - self.modeStartTime - FULL_ROTATION >= 1.5):
                print("return to sample search")
                self.turnDir = self.turnDir * -1 
                self.modeStartTime = time.time()
        else:
            v = 0
            w = 0.5 * self.turnDir

    def searchSample(self, state):          
        if (not self.isEmpty(state.sampleRB)):
            v, w = 0, 0
            self.rock_obstacle = True
            self.stateMode = NAV_SAMPLE
        elif (time.time() - self.modeStartTime >= FULL_ROTATION): 
            print("moving around")
            v, w = self.navigate([0.2, 0], state)
            if (time.time() - self.modeStartTime - FULL_ROTATION >= 1.5):
                print("return to spin")
                self.turnDir = self.turnDir * -1 
                self.modeStartTime = time.time()
        else:
            v = 0
            w = 0.5 * self.turnDir

        return v, w

    # robot spins, moves forward, spins again
    def searchLander(self, state):
        print("search lander")
        if (not self.isEmpty(state.landerRB)):
            v, w = 0, 0
            self.rock_obstacle = True
            self.stateMode = NAV_LANDER
        elif (time.time() - self.modeStartTime >= FULL_ROTATION): 
            print("moving around")
            v, w = self.navigate([0.2, 0], state)
            if (time.time() - self.modeStartTime - FULL_ROTATION >= 1.5):
                print("return to spin")
                self.modeStartTime = time.time()
        else:
            v = 0
            w = 0.5 * self.turnDir
        return v, w

    def searchRock(self, state):
        print("searching for rock")
        if (not self.isEmpty(state.rocksRB)):
            v, w = 0, 0
            self.rock_obstacle = False
            self.stateMode = NAV_SAMPLE
        elif (time.time() -self.modeStartTime >= FULL_ROTATION):
            print("moving around")
            v = 0.5
            w = 0
            if (time.time() - self.modeStartTime - FULL_ROTATION >= 2):
                print("return to spin")
                self.modeStartTime = time.time()
        else:
            v = 0
            w = 0.5 * self.turnDir
        return v, w

    def navSample(self, state):
        print("nav to sample ")
        if (self.isEmpty(state.sampleRB)):
            if (self.isEmpty(state.prevSampleRB)):
                v, w = 0, 0
                print("returing to sample search")
                self.modeStartTime = time.time()
                self.stateMode = SEARCH_SAMPLE
            else:
                v, w = 0, 0
                # find bearing of previous sample and spin that direction
                self.turnDir = np.sign(state.prevSampleRB[0][1])
                print("returning to sample search")
                self.modeStartTime = time.time()
                self.stateMode = SEARCH_SAMPLE
        else:
            currSample = state.prevSampleRB[0]
            print(currSample)
            v, w = self.navigate(currSample, state)
            if (currSample[0] < ROT_DISTANCE):
                print("acquiring sample")
                v, w = 0, 0
                self.modeStartTime = time.time()
                self.stateMode = ACQUIRE_SAMPLE

        return v, w

    def navRock(self, state):
        print("nav to  rock ")
        if (self.isEmpty(state.rocksRB)):
            if (self.isEmpty(state.prevRocksRB)):
                v, w = 0, 0
                self.turnDir = np.sign(state.prevRocksRB[0][1])
                print("returning to rock search")
                self.modeStartTime = time.time()
                self.stateMode = SEARCH_ROCK
        else:
            v, w = 0,0
            if not self.isEmpty(state.rocksRB):
                currRock = state.rocksRB[0]
                v, w = self.navigate(currRock, state)
                if (currRock[0] < FLIP_DISTANCE):
                    print("flipping rock")
                    v, w = 0, 0
                    self.modeStartTime = time.time()
                    self.stateMode = FLIP_ROCK

        return v, w
    
    def flipRock(self, state):
        print("flipping rock")
        self.rotState = OPEN
        self.modeStartTime = time.time()
        self.isBlind = True
        if (self.isBlind):
            print("cover open, driving straight")
            if (time.time() - self.modeStartTime < ROT_ACQUIRE_SAMPLE):
                v = 0.07
                w = 0
            else:
                print("closing cover")
                self.isBlind = False
                self.rotStateClose = CLOSE
        else:
            if (state.sampleCollected):
                self.modeStartTime = time.time()
                self.stateMode = SEARCH_LANDER
            else:
                self.modeStartTime = time.time()
                self.stateMode = SEARCH_SAMPLE

        return v, w

    def navLander(self, state):
        if (not state.sampleCollected):
            v, w = 0, 0
            print("sample lost, searching for sample")
        if self.isEmpty(state.landerRB):
            v, w = 0, 0
            if (not self.isEmpty(state.prevLanderRB)):
                if (state.prevLanderRB[0][0] < LANDER_SWITCH_RANGE): #maybe bearing condition
                    print("switching lander mask")
                    self.modeStartTime = time.time()
                    self.stateMode = UP_LANDER
                self.turnDir = np.sign(state.prevLanderRB[0][1])

            print("searching for lander")
            self.modeStartTime = time.time()
            self.stateMode = SEARCH_LANDER

        else:
            v, w = self.navigate(state.landerRB[0], state)

        return v,w
    
    def acquireSample(self, state):
        # centre sample
        if (not self.isEmpty(state.sampleRB) and not (-0.05 <= state.sampleRB[0][1] <= 0.05)):
            print("centering")
            self.centering = True
            sample = state.sampleRB[0]
            w = sample[1] * 1.4
            v = 0
        elif (not self.isEmpty(state.sampleRB) and not self.isBlind):
            self.centering = False
            print("opening rot")
            v, w = 0, 0
            self.rotState = OPEN
            self.isBlind = True
            self.modeStartTime = time.time()
        elif (self.isBlind):
            if (time.time() - self.modeStartTime < 3):
                print("trying to drive straight YEEEEETTTT")
                v = 0.07
                w = 0
            else:
                v, w = 0, 0
                self.rotState = CLOSE
                self.isBlind = False
        elif (not self.isBlind):
            self.rotState = CLOSE
            if (state.sampleCollected):
                print("sample collected, search lander")
                v, w = 0, 0
                self.modeStartTime = time.time()
                self.stateMode = SEARCH_LANDER
            else:
                print("sample lost, searching sample")
                v, w = 0, 0
                self.modeStartTime = time.time()
                self.stateMode = SEARCH_SAMPLE
        return v, w

    def driveUpLander(self,state):
        print("drive up lander")
        v = 0.85
        w = 0
        if (time.time()- self.modeStartTime >= 1.5):
            if (not self.isEmpty(state.sampleRB)):
                if (state.sampleRB[0][0] < 0.1):
                    v, w = 0, 0
                    self.modeStartTime = time.time()
                    self.stateMode = HOLE_ALIGN
        return v, w

    def holeAlign(self, state):
        print("centering hole")
        if (not self.isEmpty(state.sampleRB)):
            if (not (-0.05 <= state.sampleRB[0][1] <= 0.05)):
                print("centering hole")
                self.centering = True
                hole = state.sampleRB[0]
                w = hole[1] * 1.4
                v = 0
            else:
                v, w = 0, 0
                self.modeStartTime = time.time()
                self.stateMode = SAMPLE_DROP

    def dropSample(self, state):
        if (state.sampleCollected):
            v = 0.1
            w = 0
        else:
            v, w = 0,0
            self.numSampleCollected += 1
            self.stateMode = SEARCH_SAMPLE



                


#-----------------------#
# Navigation functions
#-----------------------#

    def navigate(self, goal, state):
        vRep, wRep = 0, 0
        v = KV_ATTRACT * goal[0]
        w = KW_ATTRACT * goal[1]
        vRep, wRep = self.avoidObstacles(state)
        v = v - vRep
        w = w- wRep
        return v, w

    def avoidObstacles(self, state):
        allObstacles = []
        obstacles = state.obstaclesRB#[[r,b], [r,b]]
        rocks = state.rocksRB #[[r,b], [r,b]]
        vRep = 0
        wRep = 0
        if not self.isEmpty(obstacles):
            print("adding obstacles")
            obstacles = obstacles.tolist()
            allObstacles = allObstacles + obstacles
            print(allObstacles)
        if not self.isEmpty(rocks) and self.rock_obstacle:
            print("adding rocks")
            rocks = rocks.tolist()
            allObstacles = allObstacles + rocks
            print(allObstacles)
            
        if not self.isEmpty(allObstacles):
            closeObs = self.closestObstacle(allObstacles)
            if closeObs[0] < 0.5:
                wRep =  (np.sign(closeObs[1]) * (0.5 - closeObs[0]) * (3 - abs(closeObs[1]))* KW_REPULSE)
                vRep =  (0.5 - closeObs[0]) * 0.2
                if closeObs[0] < 0.4:
                    wRep = 2 * wRep
        return vRep, wRep

    def closestObstacle(self, obstacles):
        minObstacle = obstacles[0]
        for obstacle in obstacles:
            if (obstacle[0] < minObstacle[0]):
                minObstacle = obstacle
        return minObstacle


#-----------------------#
# Helper functions
#-----------------------#
    def isEmpty(self, objectIn): #check to see if object is empty, suitable for sim and real life
        if (type(objectIn) != np.ndarray):
            if (objectIn is None or objectIn == []):
                return True
            else:
                return False
        else:
            empty = objectIn.size == 0
        return empty

    def ROTCollect(self, state):
        self.rotState = OPEN
        v = 0.05
        w = 0

        return v, w



    def driveForward(self):
        print("drive forward")
        driveStart = time.time()
        if (time.time() - driveStart < 2):
            v = 0.2
            w = 0
        else:
            v = 0
            w = 0
        return v, w
    def driveBack(self):
        print("drive reverse")
        if (time.time() - self.modeStartTime < 2):
            v = -0.2
            w = 0
        else:
            v = 0
            w = 0
        return v, w



    def driveOffLander(self, state):
        v = 0.2
        w = 0
        if(time.time() - self.modeStartTime >= DRIVE_OFF_TIME):
            v = 0
            w = 0
            self.modeStartTime = time.time()
            state.onLander = False
        return v, w
