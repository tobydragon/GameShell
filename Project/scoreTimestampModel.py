__author__ = 'Kevin Pomer'

import time
##could import datetime to reformat to date style
class Timestamp:
    def __init__(self, score):
        self.timestamp = time.time()
        self.scoreValue = score

    def getTime(self):
        return self.timestamp

    def getScore(self):
        return self.scoreValue