__author__ = 'Kevin Pomer'
import calculateKnowledgeScore

class UnitTestModel:
    def __init__(self):
        self.timeStamp_Window = 10

        self.tagCompetentThreshold = 0.8
        self.tagIncompetentThreshold = 0.2

        self.individualCompetentThreshold = 6
        self.individualIncompetentThreshold = -6

        self.computeScore = calculateKnowledgeScore.computeWeightedScore ##Select method of computing score (Avg or weighted)

    def getTimeStampWindow(self):
        return self.timeStamp_Window

    def getTagCompetentThreshold(self):
        return self.tagCompetentThreshold

    def getTagIncompetentThreshold(self):
        return self.tagIncompetentThreshold

    def getIndividualCompetentThreshold(self):
        return self.individualCompetentThreshold

    def getIndividualIncompetentThreshold(self):
        return self.individualIncompetentThreshold

    def getComputeScore(self):
        return self.computeScore

        #other fields?

    ##Getters (No Setters because Immutable)


class PlayTestModel:
    def __init__(self):
        self.timeStamp_Window = 3

        self.tagCompetentThreshold = 0.8
        self.tagIncompetentThreshold = 0.2

        self.individualCompetentThreshold = 2
        self.individualIncompetentThreshold = -2

        self.computeScore = calculateKnowledgeScore.computeAverageScore ##Select method of computing score (Avg or weighted)

    def getTimeStampWindow(self):
        return self.timeStamp_Window

    def getTagCompetentThreshold(self):
        return self.tagCompetentThreshold

    def getTagIncompetentThreshold(self):
        return self.tagIncompetentThreshold

    def getIndividualCompetentThreshold(self):
        return self.individualCompetentThreshold

    def getIndividualIncompetentThreshold(self):
        return self.individualIncompetentThreshold

    def getComputeScore(self):
        return self.computeScore

        #Other fields?