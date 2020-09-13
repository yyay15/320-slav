import time
import numpy as np
from math import * 
import matplotlib.pyplot as plt

#Mode 
SEARCH_SAMPLE = 1
SEARCH_ROCK = 2
NAV_SAMPLE = 3
NAV_ROCK = 4
SEARCH_LANDER = 5
NAV_LANDER = 6
ACQUIRE_SAMPLE = 7
DRIVE_UP = 8

CAMERA_BLIND = 0.2
DRIVE_OFF_TIME = 6
FULL_ROTATION = 32

KV_ATTRACT = 0.7
KW_ATTRACT = 0.8
KV_REPULSE = 1
KW_REPULSE = 0.4
class Navigation:
    def __init__(self):
        self.stateMode = SEARCH_SAMPLE
        self.modeStartTime = time.time()
        self.prevstate = SEARCH_SAMPLE
        self.turnDir = 1
        
    
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
                w = 0.2 * self.turnDir


        if (state.sampleRB != None):
            self.prevstate = self.stateMode
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
            elif(state.prevSampleRB[0][0] < CAMERA_BLIND and (state.prevSampleRB[0][1] <0.1 and state.prevSampleRB[0][1] > 0.1)):
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
            currSample = state.sampleRB[0]
            #print(currSample)
            # v, attF = self.attractivePotential(currSample)
            # repF = self.repulsivePotential(state)
            # F = (attF + repF)
            # print(F)
            # w = F * 5
            # v = v
            # v = vA -vR
            # w = wA - wR
            # v = 0.5* currSample[0]
            # w = currSample[1]
            v, w = self.totalPotential(currSample, state)
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
            v, w = self.totalPotential(state.landerRB, state)
        return v,w
    def acquireSample(self, state):
        if (not state.sampleCollected):
            v = 0.1
            w = 0
        elif (time.time() - self.modeStartTime >= 2):
            v = 0
            w = 0
            self.stateMode = SEARCH_SAMPLE
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
            v = 0.5
            w = 0
        else:
            v = 0
            w = 0
        return v, w

    def totalPotential(self, goal, state):
        attractive = self.attractivePotential(goal)
        repulsive = self.repulsivePotential(state)
        print("r:", repulsive)
        print("aL:", attractive)
        totalForce = attractive + repulsive
        v = max(0.2 * exp(-0.8*repulsive) - 0.05, 0)
        w = totalForce * 5
        print(w)
        return v, w

    def attractivePotential(self, goal):
        #v = 0.5 * KV_ATTRACT * goal[0]**2 
        attractive = 0.5 * KW_ATTRACT * (goal[1])**2 * (exp(-0.4 * goal[0]) + 0.1)
        return attractive
    def repulsivePotential(self, state):
        repulsive = 0
        c3 = 2
        c4 = 2
        obstacles = state.obstaclesRB

        if obstacles != None:
            minObstacle = obstacles[0]
            # for obstacle in obstacles:
            #     if obstacle[0] < minObstacle[0]:
            #         minObstacle = obstacle
            dO = minObstacle[0]
            hO = minObstacle[1]
            if dO < 0.5:
                
                #repulsive = 0.1* (1/0.01 - 1/(dO))
                #repulsive =  KW_REPULSE * ((c3 * abs(hO))+1/ c3**2) * exp(-c3*abs(3-hO))* exp(-c4*dO)
                repulsive =  KW_REPULSE * ((c3 * abs(hO))+1/ c3**2) * exp(-c3*abs(hO))* exp(-c4*dO)
        
        return repulsive
