__author__ = 'Kevin Pomer'

import time
##could import datetime to reformat to date style
class Timestamp:
    def __init__(self, maxScores):
        self.scores = []
        self.timeStamps = []

        self.maxScores = maxScores
        ##maximum number of scores to hold onto

    def addScore(self, newScore):
        time = self.getTime()
        if (len(self.scores)>=self.maxScores):
            for i in range(0, self.maxScores-2):
                self.scores[i] = self.scores[i+1]
                self.timeStamps[i] = self.timeStamps[i+1]
            del self.scores[self.maxScores - 1]
            del self.timeStamps[self.maxScores-1]

        self.scores.append(newScore)
        self.timeStamps.append(time)

    def getTime(self):
        return time.time()

    def toKnowledgeModel(self):
        return self.scores, self.timeStamps