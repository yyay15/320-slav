# Stores current state and state stateMachine
#Mode 
# SEARCH_SAMPLE = 0
# SEARCH_ROCK = 1
# NAV_SAMPLE = 2
# NAV_ROCK = 3
# ACQUIRE_SAMPLE = 4
# LIFT_ROCK = 5

# class state:
#     def __init__(self):
#         self.sampleRB = None
#         self.landerRB = None
#         self.obstaclesRB = None
#         self.rocksRB = None
#         self.currentState = SEARCH_SAMPLE

#     def stateMachine(self):
#         if (sampleRB == None):

import navigation

nav = navigation.Navigation()
nav.updateVelocities()
