import numpy as np

WHEELRADIUS = 0.03 # Metres
WHEELBASE = 0.13    # Metres

class Localisation:
    def __init__(self):
        self.wL = 0
        self. wR = 0
        position = np.zeros((3, 1)) # x, y, theta
        deltaPos = np.zerps((3, 1)) #dot{ x, y, theta }
    
    def getWheelAngVel(self, wL, wR, w):
        self.wL = wL
        self.wR = wR
        
    
    def calculateTransform(self):
