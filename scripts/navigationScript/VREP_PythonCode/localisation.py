import numpy as np
import time 
from math import *

WHEELRADIUS = 0.03 # Metres
WHEELBASE = 0.13    # Metres

class Localisation:
    def __init__(self):
        self.wL = 0
        self. wR = 0
        self.position = np.zeros((3, 1)) # x, y, theta
        self.deltaPos = np.zeros((3, 1)) #dot{ x, y, theta }
        self.timer = time.time()
    
    def getWheelAngVel(self, v, w):
        # self.wL = wL
        # self.wR = wR
        # v1 = wR * WHEELRADIUS
        # v2 = wL * WHEELRADIUS
        # w1 = v1/(WHEELBASE)
        # w2 = v2/ (WHEELBASE)
        # v = WHEELBASE/2 * (w1 - w2)
        # print("Velc", v)
        # w = w1 + w2
        # w = 0.15
        deltaTime = time.time() - self.timer
        self.calculateTransform(v, w, deltaTime)
        self.timer = time.time()

        
    
    def calculateTransform(self, v, w, deltaTime):
        theta = w*deltaTime - self.deltaPos[2]
        state = np.array([v, w])
        state = np.vstack(state)
        transform = np.array([[cos(theta), 0], [sin(theta), 0], [0, 1]])
        self.deltaPos = np.matmul(transform, state)
        self.position = self.position + self.deltaPos * deltaTime
