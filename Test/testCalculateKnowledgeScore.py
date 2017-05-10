from unittest import TestCase
import calculateKnowledgeScore
from assessmentEventModel import AssesmentEvent

class testScores(TestCase):

    def createEvents(self):
        a1 = AssesmentEvent(5)
        a2 = AssesmentEvent(6)
        a3 = AssesmentEvent(7)
        a4 = AssesmentEvent(8)
        a5 = AssesmentEvent(9)
        a6 = AssesmentEvent(10)
        eventsList = [a1, a2, a3, a4, a5, a6]
        reverseEventsList = [a6, a5, a4, a3, a2, a1]
        return [eventsList, reverseEventsList]

    def testAverage(self):
        list = self.createEvents()[0]
        reverseList = self.createEvents()[1]
        l1 = [list[0]]

        self.assertEqual(calculateKnowledgeScore.computeAverageScore(l1), 5)
        self.assertEqual(calculateKnowledgeScore.computeWeightedScore(l1), 5)

        self.assertEqual(calculateKnowledgeScore.computeAverageScore(list), 7.5)
        self.assertEqual(calculateKnowledgeScore.computeWeightedScore(list), (8 + (1/3))) ##Round for weighting 8.333...
        self.assertEqual(calculateKnowledgeScore.computeAverageScore(reverseList), 7.5)
        self.assertEqual(calculateKnowledgeScore.computeWeightedScore(reverseList), (6 + (2/3))) ##6.666...
