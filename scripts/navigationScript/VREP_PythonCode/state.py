
class State:
    def __init__(self):
        self.sampleRB = None
        self.landerRB = None
        self.obstaclesRB = None
        self.rocksRB = None

    def updateState(self, objects):
        self.sampleRB = objects[0]
        self.landerRB = objects[1]
        self.landerRB = objects[2]
        self.rocksRB = objects[3]

