
class State:
    def __init__(self):
        self.sampleRB = None
        self.landerRB = None
        self.obstaclesRB = None
        self.rocksRB = None
        
        self.prevSampleRB = None
        self.prevLanderRB = None
        self.prevObstaclesRB = None
        self.prevRocksRB = None

        self.onLander = True
        self.sampleCollected = True


    def updateState(self, objects, sampleCollected):
        self.prevSampleRB = self.sampleRB
        self.prevLanderRB = self.landerRB
        self.prevObstaclesRB = self.obstaclesRB
        self.prevRocksRB = self.rocksRB

        self.sampleRB = objects[0]
        self.landerRB = objects[1]
        self.obstaclesRB = objects[2]
        self.rocksRB = objects[3]
        
        self.sampleCollected = sampleCollected
