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

CAMERA_BLIND = 0.1
DRIVE_OFF_TIME = 6
FULL_ROTATION = 32

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
                            
        if (state.onLander): # change this to false in real life
            v,w = self.driveOffLander(state)
        else:
            if (time.time() -self.modeStartTime >= FULL_ROTATION):
                v, w = self.driveForward()
            else:
                v = 0
                w = 0.2


        if (state.sampleRB != None):
            self.stateMode = 3
        
        return v, w

    def navSample(self, state):
        print(state.sampleRB)
        if (state.sampleRB == None):
            if (state.prevSampleRB == None):
                v = 0
                w = 0
                print("returing to sample search")
                self.stateMode = SEARCH_SAMPLE
            elif(state.prevSampleRB[0][0] < CAMERA_BLIND):
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





    def navRock(self):
        print(1)

    def navLander(self, state):
        print(state.landerRB)
        if (not state.sampleCollected):
            v = 0 
            w = 0
            print("sample lost, searching for sample")
        if state.landerRB == None and state.sampleCollected:
            if(state.prevLanderRB[0]< 0.5):
                print ("drive up sample")
                v = 0
                w = 0
                self.stateMode = DRIVE_UP
            elif (state.landerRB == None):
                v = 0
                w = 0
                print("returning to lander search")
                self.stateMode = SEARCH_LANDER
            else:
                v = 0
                w = 0

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
        if(time.time() - self.modeStartTime >= DRIVE_OFF_TIME):
            v = 0
            w = 0
            self.modeStartTime = time.time()
            state.onLander = False
        return v, w
    def avoidObstacles(self,state, v, w):
        if state.obstaclesRB != None:
            for obstacle in obstaclesRB:
                if obstacle[0] < 1:
                    v = v -(0.5 - obstacle[0]) * 0.1
                    w = w - np.si
        

    def driveForward(self):
        print("drive forward")
        driveStart = time.time()
        if (time.time() - driveStart < 2):
            v = 0.5
            w = 0
        else:
            v = 0
            w = 0
        return v, w

    

    
