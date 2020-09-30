import numpy as np
from math import * 
import time 

RUN_TIME = 1
class Localisation:
    def __init__(self):
        self.v = 0
        self.w = 0
        self.x = 0
        self.y = 0
        self.theta = 0
        self.startTime = time.time()

    def getRangeBearing(self, v, w):
        deltaTime = time.time() - self.startTime
        self.theta += w * deltaTime 
        thetaD = self.theta * (180/pi)
        print(thetaD % 360)
        # self.x += v * cos(theta)
        # self.y += v * sin(theta)
        self.startTime = time.time()
        #print("x", self.x, "y", self.y)