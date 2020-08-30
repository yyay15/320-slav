import time

#Mode 
SEARCH_SAMPLE = 1
SEARCH_ROCK = 2
NAV_SAMPLE = 3
NAV_ROCK = 4
SEARCH_LANDER = 5
NAV_LANDER = 6


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
        # v = 0
        # w = 0
        if (state.onLander):
            v,w = self.driveOffLander(state)
        else:
            v = 0
            w = 0.2
            # if (time.time() -self.modeStartTime >= 5):
            #     w = w * -1

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
                self.stateMode = 1
            else:
                currSample = state.prevSampleRB[0]
                v = 0.5* currSample[0]
                w = currSample[1]
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
        return v,w

    def searchRock(self):
        print(1)





    def navRock(self):
        print(1)

    def navLander(self):
        print(1)
    def acquireSample(self):
        print(1)

    def driveOffLander(self, state):
        v = 0.2
        w = 0
        if(time.time() - self.modeStartTime >= 6):
            v = 0
            w = 0
            self.modeStartTime = time.time()
            state.onLander = False
        return v, w
