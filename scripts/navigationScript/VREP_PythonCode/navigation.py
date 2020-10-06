import time

#Mode 
SEARCH_SAMPLE = 1
SEARCH_ROCK = 2
NAV_SAMPLE = 3
NAV_ROCK = 4
SEARCH_LANDER = 5
NAV_LANDER = 6
ACQUIRE_SAMPLE = 7
DRIVE_UP = 8

camera_blind = 0.1

class Navigation:
    def __init__(self):
        self.stateMode = SEARCH_SAMPLE
        self.modeStartTime = time.time()
    
    def currentState(self, stateNum):
        switchState = {
            1: self.searchSample,
            2: self.searchRock,
            3: self.navSample, 
            4: self.navRock, 
            5: self.searchLander,
            6: self.navLander,
            7: self.acquireSample,
            8: self.driveUpLander
        }
        return switchState.get(stateNum, self.searchSample)

    def updateVelocities(self, state):
        v, w = self.currentState(self.stateMode)(state)
        return v, w


    def searchSample(self, state):
        # print("search sample")
        # v = 0
        # w = 0
        if (state.onLander):
            v,w = self.driveOffLander(state)
        else:
            v = 0
            w = 0.2
            # if (time.time() -self.modeStartTime >= 5):
            #     w = w * -1

<<<<<<< HEAD
        if (state.sampleRB != None):
            self.stateMode = 3
        
=======
    # robot spins, moves forward, spins again
    def searchLander(self, state):
        print("search lander")
        if (not self.isEmpty(state.prevLanderRB)):
            self.turnDir = np.sign(state.prevLanderRB[0][1])
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
>>>>>>> 71c137f058b9a4ea1501c270b0f32cff487bc19a
        return v, w

    def navSample(self, state):
        print(state.sampleRB)
        if (state.sampleRB == None):
            if (state.prevSampleRB == None):
                v = 0
                w = 0
                print("returing to sample search")
                self.stateMode = SEARCH_SAMPLE
            elif(state.prevSampleRB[0][0] < camera_blind):
                print ("acquiring sample")
                v = 0
                w = 0
                self.stateMode = ACQUIRE_SAMPLE
            else:
                v = 0
                w = 0

        else:
            currSample = state.sampleRB[0]
            v = 0.5* currSample[0]
            w = currSample[1]

        #print("navigating to sample")
        return v, w

    def searchLander(self, state):
        v = 0
        w = 0.2
        if (state.landerRB != None):
            print(state.landerRB)
            v = 0
            w = 0
            self.stateMode = NAV_LANDER
        return v,w

    def searchRock(self):
        print(1)

<<<<<<< HEAD

=======
    def navLander(self, state):
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
>>>>>>> 71c137f058b9a4ea1501c270b0f32cff487bc19a


        return v,w
    
    def acquireSample(self, state):
        # centre sample
        if (not self.isEmpty(state.sampleRB) and not (-0.05 <= state.sampleRB[0][1] <= 0.05)):
            print("centering")
            self.centering = True
            sample = state.sampleRB[0]
            w = sample[1] * 1.15
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
                self.stateMode = DRIVE_UP
            elif (state.landerRB == None):
                v = 0
                w = 0
                print("returning to lander search")
                self.stateMode = SEARCH_LANDER
            else:
<<<<<<< HEAD
                v = 0
                w = 0
=======
                print("sample lost, searching sample")
                v, w = 0, 0
                if (not self.isEmpty(state.prevSampleRB)):
                    self.turnDir = np.sign(state.prevRocksRB[0][1])
                self.modeStartTime = time.time()
                self.stateMode = SEARCH_SAMPLE
        return v, w

    def driveUpLander(self,state):
        print("drive up lander")
        if (not self.isEmpty(state.landerRB)):
            self.rotState = SLIGHT_OPEN
            v = 0.7
            w = state.landerRB[0][1]
            #if (time.time()- self.modeStartTime >= 1.5):
        else:
            v, w = 0, 0
            self.modeStartTime = time.time()
            self.stateMode = SEARCH_LANDER

        return v, w
    
    def alignRock(self, state):
        print("aligning rock")
        v, w = 0, 0
        if (not self.isEmpty(state.rotHoleRB)):
            rotHoleBearing = state.rotHoleRB[0][1]
            rotHoleBearing = (rotHoleBearing) * 1.1
            if (-0.03 <= rotHoleBearing <= 0.03):
                print("changing to flip")
                v, w = 0, 0
                self.modeStartTime = time.time()
                self.stateMode = FLIP_ROCK
>>>>>>> 71c137f058b9a4ea1501c270b0f32cff487bc19a

        else:
            if (state.landerRB[0] < 0.4):
                v = state.landerRB[0]
            else:
                v = 0.5* state.landerRB[0]
            w = state.landerRB[1]
        return v,w
    def acquireSample(self, state):
        if (not state.sampleCollected):
            v = 0.1
            w = 0
        
        else:
            v = 0
            w = 0
            print("searching for lander")
            self.stateMode = SEARCH_LANDER
        return v, w
    def driveUpLander(self,state):
        v = 0.5
        w = 0
        return v, w
    def driveOffLander(self, state):
        v = 0.2
        w = 0
        if(time.time() - self.modeStartTime >= 6):
            v = 0
            w = 0
            self.modeStartTime = time.time()
            state.onLander = False
        return v, w
