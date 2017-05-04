from unittest import TestCase
from calculateKnowledgeScore import CalculateScore
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
        return eventsList

    def testAverage(self):
        compute = CalculateScore()
        list = self.createEvents()
        l1 = [list[0]]

        self.assertEqual(compute.computeAverageScore(l1), 5)
        self.assertEqual(compute.computeWeightedScore(l1), 5)
