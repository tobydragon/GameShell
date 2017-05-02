__author__ = 'Kevin Pomer'
import assessmentEventModel
from stageController import CardStateInfo

class CalculateScore:

    def computeAverageScore(self, events):
        totalScore = 0
        if len(events) == 0:
            return 0 ##Must be 0 for calcQuestionTagTypeScore()
        else:
            for i in events:
                score = i.getScore()
                totalScore = totalScore + score

        totalScore = totalScore/(len(events))
        return totalScore

    def computeWeightedScore(self, events):
        weight = 1
        length = len(events)
        weightDivisor = 2^length
        scoreDict = {}
        if length == 0:
            return 0  ##Must be 0 for calcQuestionTagTypeScore()
        else:
            for i in events:
                score = i.getScore()
                scoreDict[score] = weight
                weight = weight * 2
        totalScore = 0
        for s in scoreDict:
            totalScore = totalScore + (s*scoreDict[s])
        totalScore = totalScore/weightDivisor
        return totalScore
