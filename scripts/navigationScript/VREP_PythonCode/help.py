import numpy as np
obstacles = np.array([[1, 2], [3,4]])
obstacles = obstacles.tolist()
print(obstacles)
allObstacles = []
print(allObstacles + obstacles)

#print(np.append([], [[1,2], [3,4]], axis=0))
