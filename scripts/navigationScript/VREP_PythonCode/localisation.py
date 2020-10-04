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
        self.sampleGlobal = None
        self.rockGlobal = None 
        self.state = None
    
    def getWheelAngVel(self, v, w, state):
        self.state = state
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



    def objectToGlobal(self, objects):
        objectXY = []
        for item in objects:
            objectX = item[0] * cos(item[1])
            objectY = item[0] * sin(item[1])
            objectX = objectX + self.position[0]
            objectY = objectY + self.position[1]
            objectXY.append([objectX, objectY])
        return objectXY
    
    # def updateExisiting(self, objectXY):
    #     for coord in objectXY
        



