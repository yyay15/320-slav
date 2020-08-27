#Mode 
SEARCH_SAMPLE = 1
SEARCH_ROCK = 1
NAV_SAMPLE = 2
NAV_ROCK = 3
ACQUIRE_SAMPLE = 4
LIFT_ROCK = 5

class Navigation:
    def __init__(self):
        self.state = SEARCH_SAMPLE
    
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

    def updateVelocities(self):
        v, w = self.currentState(self.state)()
        return v, w


    def searchSample(self):
        print("search sample")
        v = 0
        w = 0.1
        return v, w
        
    def searchRock(self):
        print(1)
    def navSample(self):
        print(1)
    def navRock(self):
        print(1)
    def searchLander(self):
        print(1)
    def navLander(self):
        print(1)
    def acquireSample(self):
        print(1)