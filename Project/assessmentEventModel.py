__author__ = 'Kevin Pomer'

import time
##could import datetime to reformat to date style
class AssesmentEvent:
    def __init__(self, score):
        self.timestamp = time.time()
        self.scoreValue = score

        #Currently 1-10 used in computeScore() in knowledgeModel.py
        #self.difficulty = difficulty

    def getTime(self):
        return self.timestamp

    def getScore(self):
        return self.scoreValue
