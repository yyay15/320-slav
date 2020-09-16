import time
import numpy as np
from math import * 


KV_ATTRACT = 0.7
KW_ATTRACT = 0.8
KV_REPULSE = 1
KW_REPULSE = 0.1
c3 = 3
c4 = 4
goal = [0.44, -0.31]
hO = -0.2
dO = 0.1
attractive = np.sign(goal[1])*0.5 * KW_ATTRACT * (goal[1])**2 * (exp(-0.4 * goal[0]) + 0.1)
repulsive =  KW_REPULSE * ((c3 * abs(hO))+1/ c3**2) * exp(-c3*abs(hO))* exp(-c4*dO)
F = attractive + repulsive
print(attractive*5)
print(repulsive)
print(F)
print(5*F)
