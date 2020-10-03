import time
import math
import numpy as np
import sys

import localisation

loc = localisation.Localisation()


if __name__ == '__main__':
    for i in range(0, 20):
        v = 0.1
        w = 0.2
        loc.getWheelAngVel(v, w)
        print("xdot", loc.deltaPos)
        print("x", loc.position)
