import time

#Mode 
SEARCH_SAMPLE = 1
SEARCH_ROCK = 1
NAV_SAMPLE = 2
NAV_ROCK = 3
ACQUIRE_SAMPLE = 4
LIFT_ROCK = 5

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
            7: self.acquireSample
        }
        return switchState.get(stateNum, self.searchSample)

    def updateVelocities(self, state):
        v, w = self.currentState(self.stateMode)(state)
        return v, w


    def searchSample(self, state):
        # print("search sample")
        v = 0
        w = 0.2
        if(time.time() - self.modeStartTime >= 20):
            w = -0.2
        if (state.sampleRB != None):
            self.stateMode = 3
        
        return v, w

    def navSample(self, state):
        if (state.sampleRB == None):
            v = 0
            w = 0
            self.stateMode = 1
        else:
            currSample = state.sampleRB[0]
            v = 0.5* currSample[0]
            w = currSample[1]

        #print("navigating to sample")
        return v, w

    def searchRock(self):
        print(1)





    def navRock(self):
        print(1)
    def searchLander(self):
        print(1)
    def navLander(self):
        print(1)
    def acquireSample(self):
        print(1)