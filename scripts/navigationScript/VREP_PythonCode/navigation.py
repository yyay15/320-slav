import time
import numpy as np
from math import * 

# STATES
SEARCH_ALL = 0
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
ROCK_ALIGN = 12
ALIGN_LANDER = 13
FLIP_CHECK = 14

#ROT CONSTANTS
# State 0 = pass
# State 1 = Open
# State 2 = Close
# State 3 = Slight Open
# State 4 = Hard Close
# State 5 = Drop Sample
PASS_STATE = 0
OPEN = 1
CLOSE = 2
SLIGHT_OPEN = 3
HARD_CLOSE = 4
DROP_SAMPLE = 5

# DISTANCE/TIME VARIABLES
ROT_DISTANCE = 0.22 #collect distance 
FLIP_DISTANCE = 0.16
ROCK_ALIGN_DISTANCE = 0.25
FULL_ROTATION = 15
ROT_ACQUIRE_SAMPLE = 0.9
DRIVE_OFF_TIME = 6
LANDER_SWITCH_RANGE = 0.32

# OBSTACLE AVOIDANCE GAINS 
KV_ATTRACT = 0.5 #0.5
KW_ATTRACT = 1.3    #1.5 #0.8
KV_REPULSE = 0.3
KW_REPULSE = 2.5

class Navigation:
    def __init__(self):
        self.stateMode = 0 # intial start state
        self.modeStartTime = time.time() # timer for each state
        self.flipRockStart = 0
        self.searchTime= time.time()
        self.checkSampleTime = time.time()
        self.overallTime = time.time()
        self.turnDir = 1                 # turn clockwise or anticlockwise
        self.rockObstacle = True        # check if rocks should be avoided
        self.rotState = CLOSE            # state for sample collection
        self.isBlind = False
        self.centering = False
        self.commandnav = False
        self.attemptFlip = False
        self.landerHoleSeen = False
        self.onLander = True
        self.numSampleCollected = 0
        self.prevLanderAreaDiff = 0

    
    def currentState(self, stateNum):
        switchState = {
            0: self.searchAll,
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
            11: self.dropSample,
            12: self.alignRock,
            13: self.alignLander,
            14: self.checkFlip
        }
        return switchState.get(stateNum, self.searchSample)

    # calls relevant state function and returns target velocities
    def updateVelocities(self, state):
        v, w = self.currentState(self.stateMode)(state)
        return v, w

    def searchAll(self, state):
        v, w = 0, 0
        if (time.time() - self.overallTime  < 120 or self.numSampleCollected >= 1):
            self.stateMode = SEARCH_ROCK
            self.modeStartTime = time.time()
        else:
            self.stateMode = SEARCH_SAMPLE
            self.modeStartTime = time.time()
        return v, w

    def searchSample(self, state):      
        v, w = 0, 0   
        if (state.sampleCollected):
            self.rotState = CLOSE
            self.modeStartTime = time.time()
            self.stateMode =  SEARCH_LANDER
        else:
            self.rotState = SLIGHT_OPEN
            if (not self.isEmpty(state.sampleRB)):
                self.stateMode = NAV_SAMPLE
            elif (time.time() - self.modeStartTime >= FULL_ROTATION):
                if (not self.isEmpty(state.obstaclesRB)):
                    print("nav to obstacle")
                    v, w = self.navObsAvoidRock(state)
                    if (state.obstaclesRB[0][0] < 0.3):
                        self.modeStartTime = time.time()
                else:
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
        v, w = 0, 0
        self.rotState = CLOSE
        self.rockObstacle = True
        if (not self.isEmpty(state.prevLanderRB)):
            self.turnDir = np.sign(state.prevLanderRB[0][1]) 
        print("search lander")
        if (not self.isEmpty(state.landerRB)):
            v, w = 0, 0
            self.stateMode = NAV_LANDER
        elif (time.time() - self.modeStartTime >= FULL_ROTATION): 
            if (not self.isEmpty(state.wallRB)):
                if (state.wallRB[0][0] < 0.3):
                    w = 0.9 * self.turnDir
                else:
                    v, w = self.navigate([0.1, 0], state)
            else:           
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
        if (self.rotState == OPEN or self.rotState == CLOSE):
            self.rotState = SLIGHT_OPEN
        if (not self.isEmpty(state.rocksRB)):
            v, w = 0, 0
            self.rockObstacle = False
            self.stateMode = NAV_ROCK
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
            if (self.onLander):
                if time.time() - self.modeStartTime < 2.5:
                    v = 0.08
                    w = 0
                else:
                    v = 0
                    w = 0
                    self.onLander = False
            else:
                v, w = 0, 0
                if (not self.isEmpty(state.prevSampleRB)):
                    self.turnDir = np.sign(state.prevSampleRB[0][1])
                print("retunring to sample search")
                self.modeStartTime = time.time()
                self.stateMode = SEARCH_SAMPLE
        else:
            self.modeStartTime = time.time()
            currSample = state.sampleRB[0]
            v, w = self.navigate(currSample, state)
            if (currSample[0] < ROT_DISTANCE):
                print("acquiring sample")
                v, w = 0, 0
                self.modeStartTime = time.time()
                self.stateMode = ACQUIRE_SAMPLE
                self.onLander = False
        return v, w

    def navRock(self, state):
        v, w = 0, 0
        print("nav to  rock ")
        if (self.isEmpty(state.rocksRB)):
            if (not self.isEmpty(state.prevRocksRB)):
                self.turnDir = np.sign(state.prevRocksRB[0][1])
            print("returning to rock search")
            self.modeStartTime = time.time()
            self.stateMode = SEARCH_ROCK
        else:
            if not self.isEmpty(state.rocksRB):
                currRock = state.rocksRB[0]
                v, w = self.navigate(currRock, state)
                if (currRock[0] < ROCK_ALIGN_DISTANCE):
                    print("align rock")
                    self.modeStartTime = time.time()
                    if (self.rotState != CLOSE):
                        self.rotState = CLOSE
                    self.stateMode = ROCK_ALIGN

        return v, w


    def flipRock(self, state):
        #time to drive to  be in flip position
        v, w = 0, 0
        print("driving to flip pos")
        # drive straight for 1.5 seconds first 
        if (time.time() - self.modeStartTime <= 2.0):
            v = 0.042
            w = 0
            self.attemptFlip = False
        else:
            # if the cover hasnt been lifted and not attempted then flip 
            print("preparing to flip")
            v, w = 0, 0
            if (not self.isBlind and not self.attemptFlip):
                print("flipping rock")
                v, w = 0, 0
                self.rotState = OPEN
                self.flipRockStart= time.time()
                self.isBlind = True
            if (self.isBlind):
                if (time.time() - self.flipRockStart < 0.7):
                    print("cover open, reversing")
                    v = -0.07
                    w = 0
                else:
                    # after 1 second close cover
                    print("closing cover")
                    self.rotState = CLOSE
                    self.isBlind = False
                    self.attemptFlip = True
            else:
                self.rotState = CLOSE
                self.modeStartTime = time.time()
                self.stateMode = FLIP_CHECK

        return v, w
    
    def checkFlip(self, state):
        v, w = 0, 0
        if (time.time() - self.modeStartTime > 1):
            if (self.isEmpty(state.sampleRB)):
                self.modeStartTime = time.time()
                self.stateMode = SEARCH_ROCK
            else:
                self.modeStartTime = time.time()
                self.rockObstacle = False
                self.stateMode = SEARCH_SAMPLE
        return v, w



    def navLander(self, state):
        self.rotState = CLOSE
        if (not state.sampleCollected):
            v, w = 0, 0
            print("sample lost, searching for sample")
        if self.isEmpty(state.landerRB):
            v, w = 0, 0
            if (not self.isEmpty(state.prevLanderRB)):
                self.turnDir = np.sign(state.prevLanderRB[0][1])

            print("searching for lander")
            self.modeStartTime = time.time()
            self.stateMode = SEARCH_LANDER

        else:
            if (state.landerRB[0][0] < LANDER_SWITCH_RANGE):
                if (-0.05 <= state.landerRB[0][1] <= 0.05):
                    print("switching to  align lander")
                    self.modeStartTime = time.time()
                    self.stateMode = UP_LANDER
                else:
                    v = 0
                    w = w = state.landerRB[0][1] * 0.5
            landerR = state.landerRB[0][0] * 2
            landerB = state.landerRB[0][1] * 2
            v, w = self.navigate([landerR, landerB], state)

            # Alan: Adjust for slower velo and faster omega
            v = v * 0.69 
            w = w * 1.25

        return v,w
    
    def acquireSample(self, state):
        # centre sample
        if (not self.isEmpty(state.sampleRB) and not (-0.05 <= state.sampleRB[0][1] <= 0.05)):
            print("centering")
            self.centering = True
            sample = state.sampleRB[0]
            w = sample[1] 
            v = 0
        elif (not self.isEmpty(state.sampleRB) and not self.isBlind):
            self.centering = False
            print("opening rot")
            v, w = 0, 0
            self.rotState = OPEN
            self.isBlind = True
            self.modeStartTime = time.time()
        elif (self.isBlind):
            if (time.time() - self.modeStartTime < 1): #used to be 1.6
                v = 0.07
                w = 0
            else:
                v, w = 0, 0
                self.rotState = HARD_CLOSE
                self.isBlind = False
        elif (not self.isBlind):
            self.rotState = HARD_CLOSE
            if (state.sampleCollected):
                print("sample collected, search lander")
                v, w = 0, 0
                self.rockObstacle = True
                self.modeStartTime = time.time()
                self.stateMode = SEARCH_LANDER
            else:
                print("sample lost, searching sample")
                v, w = 0, 0
                if (not self.isEmpty(state.prevSampleRB)):
                    self.turnDir = np.sign(state.prevSampleRB[0][1]) 
                self.modeStartTime = time.time()
                self.stateMode = SEARCH_SAMPLE
        return v, w

# !!!!!!!!FUNCTION TO DRIVE TO THE TOP OF THE LANDER !!!!!!#
    def driveUpLander(self,state):        
        self.rotState = SLIGHT_OPEN
        self.onLander = True

        # Lets chill for a little bit 
        if (time.time() - self.modeStartTime > 1):
            print("Lets chill and vibe for a bit")
            v, w = 0, 0 


        if (state.sampleCollected):
            if (not self.isEmpty(state.holeRB)):
                self.stateMode = HOLE_ALIGN
            if (time.time() - self.modeStartTime > 4.5):
                print("Im LOST PLEASE HELP")
                v, w = 0, 0
                self.stateMode = SEARCH_LANDER
            else:
                print("Imma end this mans career")
                v = 0.075
                w = 0
        else:
            v, w = 0, 0
            self.rotState = OPEN
            print("Jobs Done")
            self.stateMode = SEARCH_SAMPLE



        if (not self.isEmpty(state.holeRB)):
             v = 0.06
             w = state.holeRB[0][1]
             self.modeStartTime = time.time()
             self.stateMode = SAMPLE_DROP
        else:
             v = 0.06
             w = 0

        return v, w
        
    def alignLander(self, state):
        self.rotState = SLIGHT_OPEN
        v, w = 0, 0
        # if (time.time() - self.modeStartTime > 0.1):
        #     v =0.15
        #     w = 0
        # else:
        if (not self.isEmpty(state.landerRB)):
            landerDiff = state.landerArea - state.prevLanderArea
            if (landerDiff < 0 and self.prevLanderAreaDiff > 0):
                self.prevLanderAreaDiff = 0
                self.modeStartTime = time.time()
                self.stateMode = UP_LANDER
            else:
                v = 0
                w = 0.3
                self.prevLanderAreaDiff = landerDiff
        else:
            print("align lander -> search lander")
            self.modeStartTime = time.time()
            self.stateMode = SEARCH_LANDER
        return v, w

    def alignRock(self,state):
        print("aligning rock")
        v, w = 0, 0
        if (not self.isEmpty(state.rocksRB)):
            closestRock = state.rocksRB[0]
            if (closestRock[0] < 0.17 and (-0.15 < closestRock[1] < 0.15)):
                self.modeStartTime = time.time()
                self.stateMode = FLIP_ROCK
            if (not -0.07 < closestRock[1] < 0.07):
                w =closestRock[1]
            if (closestRock[0] > 0.17):
                v = 0.05
        else:
            self.modeStartTime = time.time()
            self.stateMode = SEARCH_ROCK
        return v, w


    # depreciate unless 👀👀
    def holeAlign(self, state):
        print("I am aligning to da hoe")
        v, w = 0, 0
        if (state.sampleCollected):
            print("we gonna kobe into the hole")
            print("This is the kobe traj: ",state.holeRB)
            if(not self.isEmpty(state.holeRB)):
                hole = state.holeRB[0]
                v = 0.1
                w = hole[1]*1.3
            else:
                print("Here we go again")
                self.stateMode = UP_LANDER
        else:
            print("Gotta look for some orange spheres")
            self.stateMode = SEARCH_SAMPLE

        return v, w 
        

    def dropSample(self, state):
        if (state.sampleCollected):
            if (time.time() - self.modeStartTime < 0.5):
                v = 0.085
                w = 0 
                print("go forward")
            elif (0.5 < time.time() - self.modeStartTime < 2):
                self.rotState = OPEN
                v = 0.075
                w = 0
                print("opening ROT")
            elif (2 < time.time() - self.modeStartTime < 3):
                self.rotState = DROP_SAMPLE
                v = - 0.075
                w = 0
                print("going backward")
            else:
                v, w = 0, 0
                self.modeStartTime = time.time()
        else:
            v, w = 0, 0
            self.numSampleCollected += 1
            self.modeStartTime = time.time()
            self.rockObstacle = True
            self.stateMode = SEARCH_SAMPLE
        return v, w
#help


                


#-----------------------#
# Navigation functions DONT ADJUST THE BELOW FUNCTIONS 
#-----------------------#

    def navigate(self, goal, state):
        vRep, wRep = 0, 0
        v = KV_ATTRACT * goal[0] 
        w = KW_ATTRACT * goal[1]
        vRep, wRep = self.avoidObstacles(state)
        v = v - vRep
        w = w - wRep
        return v, w

    def avoidObstacles(self, state):
        obstacles = state.obstaclesRB#[[r,b], [r,b]]
        rocks = state.rocksRB #[[r,b], [r,b]]
        vRep, wRep = 0, 0
        if not self.isEmpty(obstacles):
            for obs in obstacles:
                wTemp = 0
                if obs[0] < 0.5:
                    wTemp =  (np.sign(obs[1]) * (0.5 - obs[0]) * (3 - abs(obs[1]))* KW_REPULSE)
                    vRep =  (0.5 - obs[0]) * 0.2
                #break potential fields and turn away 
                if obs[0] < 0.15:
                    wRep = 2 * wTemp
                    return vRep, wRep
                wRep += wTemp
        if not self.isEmpty(rocks) and self.rockObstacle:
            for obs in rocks:
                wTemp = 0
                if obs[0] < 0.6:
                    wTemp =  (np.sign(obs[1]) * (0.5 - obs[0]) * (3 - abs(obs[1]))* KW_REPULSE * 1.1)
                    vRep =  (0.5 - obs[0]) * 0.2
                    # if closeObs[0] < 0.15:
                    #     wTemp = 1.75 * wTemp
                wRep += wTemp
        return vRep, wRep

    def closestObstacle(self, obstacles):
        minObstacle = obstacles[0]
        for obstacle in obstacles:
            if (obstacle[0] < minObstacle[0]):
                minObstacle = obstacle
        return minObstacle

    def navObsAvoidRock(self, state):
        vRep, wRep = 0, 0
        v = state.obstaclesRB[0][0] * KV_ATTRACT
        w = state.obstaclesRB[0][1] * 0.5 #dont go to centre of obstacle
        if (not self.isEmpty(state.rocksRB)):
            if state.rocksRB[0][0] < 0.8:
                closeObs = state.rocksRB[0]
                wRep =  (np.sign(closeObs[1]) * (0.5 - closeObs[0]) * (3 - abs(closeObs[1]))* KW_REPULSE)
                vRep =  (0.5 - closeObs[0]) * 0.2
        v = v - vRep
        w = w -wRep
        return v, w

    # def navAndAvoid(self, goal, obstacle):
    #     vRep, wRep = 0, 0
    #     v = KV_ATTRACT * goal[0][0] * 0.2
    #     w = KW_ATTRACT * goal[0][1] * 3
    #     if not self.isEmpty(obstacle):
    #         vRep = (0.5 - obstacle[0][0]) * 0.1 
    #         wRep = np.sign(obstacle[0][1]) * (0.5 - obstacle[0][0]) * (3 - abs(obstacle[0][1]))
    #     v = v - vRep * 1.2
    #     w = w - wRep * 1.2
    #     return v, w

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


# nav = Navigation()
# nav.navAndAvoid([[0, 1]], [[1, 2]])
