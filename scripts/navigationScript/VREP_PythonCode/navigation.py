import time
import numpy as np
from math import * 
#import matplotlib.pyplot as plt

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
FULL_ROTATION = 15

KV_ATTRACT = 0.4
KW_ATTRACT = 1
KV_REPULSE = 0.3
KW_REPULSE = 0.8

class Navigation:
    def __init__(self):
        self.stateMode = SEARCH_SAMPLE
        self.modeStartTime = time.time()
        self.prevstate = SEARCH_SAMPLE
        self.turnDir = 1
        self.rock_obstacle = True
        
    
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
        if (state.onLander): # change this to false in real life
            v,w = self.driveOffLander(state)
        else:
            if (state.sampleRB != None and state.sampleRB):
                v, w = 0, 0
                self.rock_obstacle = True
                self.prevstate = self.stateMode
                self.stateMode = NAV_SAMPLE
            elif (time.time() -self.modeStartTime >= FULL_ROTATION+10):
                #v, w = self.driveForward()
                #vRep, wRep = self.avoidObstacles(state)
                # v = v - vRep
                # w = w- wRep
                if (state.rocksRB != None and state.rocksRB):
                    print("nav to rock")
                    self.rock_obstacle = False
                    v, w = self.navigate(state.rocksRB[0], state)
                    if state.rocksRB[0][0] < 0.2:
                        self.modeStartTime = time.time()
                else:
                    print("moving around")
                    v = 0.05
                    w = 0.2
                    # vRep, wRep = self.avoidObstacles(state)
                    # v = v - vRep
                    # w = w - wRep
            else:
                v = 0
                w = 0.7 * self.turnDir



        
        return v, w

    def navSample(self, state):
        print("searching ")
        if (state.sampleRB == None or not state.sampleRB):
            if (state.prevSampleRB == None):
                v = 0
                w = 0
                print("returing to sample search")
                self.stateMode = SEARCH_SAMPLE
            elif(state.prevSampleRB[0][0] < CAMERA_BLIND):
                print ("acquiring sample")
                v = 0
                w = 0
                self.modeStartTime = time.time()
                self.stateMode = ACQUIRE_SAMPLE
            else:
                v = 0
                w = 0
                self.turnDir = np.sign(state.prevSampleRB[0][1])
                print("returing to sample search")
                self.stateMode = SEARCH_SAMPLE
        else:
            if state.sampleRB != None and state.sampleRB:
                currSample = state.sampleRB[0]
                print(currSample)
                v, w = self.navigate(currSample, state)
                if (currSample[0] < CAMERA_BLIND):
                    print("acquiring sample")
                    v, w = 0, 0
                    self.stateMode = ACQUIRE_SAMPLE
        #print("navigating to sample")
        return v, w

    def searchLander(self, state):
        v = 0
        w = 0.4
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
        #print(state.landerRB)
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
            v, w = self.navigate(state.landerRB, state)
            w = w

        return v,w
    
    def acquireSample(self, state):
        if (state.sampleRB != None and not (-0.01 <= state.sampleRB[0][1] <= 0.01)):
            sample = state.sampleRB[0]
            w = sample[1]
            v = 0
        elif (not state.sampleCollected):
            print("here")
            v = 0.1
            w = 0
        # elif (time.time() - self.modeStartTime >= 7):
        #     v = 0
        #     w = 0
        #     self.stateMode = SEARCH_SAMPLE
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
    def navigate(self, goal, state):
        vRep, wRep = 0, 0
        v = KV_ATTRACT * goal[0]
        w = KW_ATTRACT * goal[1]
        if (goal[0]> 0.2):
            vRep, wRep = self.avoidObstacles(state)
        v = v -vRep
        w = w-wRep
        return v, w

    # def attractivePotential(self, goal):
    #     if goal[0] < 0.2:
    #         v = 0.5 * KV_ATTRACT * 0.2**2 
    #     else:
    #         v = 0.5 * KV_ATTRACT * goal[0]**2 
    #     #attractive = 0.5 * KW_ATTRACT * (goal[1])**2 * (exp(-0.3 * goal[0]) + 0.1)
    #     attractive = 0.5 * KW_ATTRACT * goal[1]**2
    #     return v, 4*attractive

    def avoidObstacles(self, state):
        obstacles = state.obstaclesRB
        rocks = state.rocksRB
        vRep = 0
        wRep = 0
        if obstacles != None:
            if rocks != None:
                obstacles = obstacles + rocks
            closeObs = self.closestObstacle(obstacles)
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

    # def repulsivePotential(self, state):
    #     repulsive = 0
    #     c3 = 2
    #     c4 = 2
    #     obstacles = state.obstaclesRB

    #     if obstacles != None:
    #         minObstacle = obstacles[0]
    #         # for obstacle in obstacles:
    #         #     if obstacle[0] < minObstacle[0]:
    #         #         minObstacle = obstacle
    #         dO = minObstacle[0]
    #         hO = minObstacle[1]
    #         if dO < 0.5:
                
    #             #repulsive = 0.1* (1/0.01 - 1/(dO))
    #             #repulsive =  KW_REPULSE * ((c3 * abs(hO))+1/ c3**2) * exp(-c3*abs(3-hO))* exp(-c4*dO)
    #             repulsive =  KW_REPULSE * ((c3 * abs(hO))+1/ c3**2) * exp(-c3*abs(hO))* exp(-c4*dO)
        
    #     return repulsive
