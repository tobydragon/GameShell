from unittest import TestCase

from knowledgeModel import KnowledgeModel
from knowledgeModel import computeScore
#from stageController import CardStateInfo

from assessmentEventModel import AssesmentEvent
from time import sleep

class TestKnowledgeScore(TestCase):

    def testTagScore(self):
        testKnowledge = KnowledgeModel({}, [])
        testKnowledge.updateQuestionTagScore("tag1", 0.5)
        self.assertEqual(0.5, testKnowledge.calcQuestionTagScore("tag1"))
        testKnowledge.updateQuestionTagScore("tag1", 0.75)
        self.assertEqual(0.625, testKnowledge.calcQuestionTagScore("tag1"))

    def testIndividualScore(self):
        #Does not use timeStamp, but instead averages all scores
        testKnowledge = KnowledgeModel({}, [])
        testKnowledge.updateIndividualScore("i1", 5.6)
        testKnowledge.updateIndividualScore("i2", 7)
        testKnowledge.updateIndividualScore("i3", -4)
        testKnowledge.updateIndividualScore("i4", 50)
        testKnowledge.updateIndividualScore("i5", 0)
        self.assertAlmostEqual(5.6, testKnowledge.calcIndividualScore("i1"))
        self.assertEqual(-4, testKnowledge.calcIndividualScore("i3"))
        testKnowledge.updateIndividualScore("i3", -5)
        testKnowledge.updateIndividualScore("i1", -4.5)
        testKnowledge.updateIndividualScore("i2", 0)
        self.assertAlmostEqual(-4.5, testKnowledge.calcIndividualScore("i3"))
        self.assertAlmostEqual(0.55, testKnowledge.calcIndividualScore("i1")) ##uses almost equal for rounding
        self.assertAlmostEqual(3.5, testKnowledge.calcIndividualScore("i2"))

    def testAssessmentEvent(self):
        #This test will be edited after timeStamp is finished being added to Individual score and tag Score in knowledgeModel
        testKnowledge = KnowledgeModel({}, [])
        beforeTime = AssesmentEvent(0)
        sleep(0.1)
        testKnowledge.updateQuestionTagScore("Tag1", 15)
        sleep(0.1)
        afterTime = AssesmentEvent(0)
        time = testKnowledge.questionTagKnowledgeScore["Tag1"][0].getTime()
        beforeTimeCorrect = 0
        afterTimeCorrect = 0

        if(beforeTime.getTime() < time):
            beforeTimeCorrect = 1

        if (afterTime.getTime() > time):
            afterTimeCorrect = 1

        self.assertEqual(1, beforeTimeCorrect)
        self.assertEqual(1, afterTimeCorrect)


    def testComputeScore(self):
      #  eventsList = []
       # e1 = AssesmentEvent(5.2, 5)
       # eventsList.append(e1)
       # self.assertEqual(5.2, computeScore(eventsList))
        test = 0 ##Not using computeScore()

    def testBuckets(self):
        testKnowledge = KnowledgeModel({}, [])
        individuals = ['i1', 'i2', 'i3']
        individualBuckets = {"Known": [], "Unknown": [], "Unclear": [], "Not Asked": individuals}
        for j in range(0, 15, 1):
            for i in individuals:
                testKnowledge.updateIndividualScore({'i1': 1, 'i2':(-1)^j, 'i3':1})
        testKnowledge.updateIndividualBuckets()

        x = 0
        if 'i1' in individualBuckets["Known"]:
            x = 1
        self.assertEqual(1, x)

        if 'i2' in individualBuckets["Unknown"]:
            x = 2
        self.assertEqual(2, x)

        if 'i3' in individualBuckets["Unclear"]:
            x = 3
        self.assertEqual(3, x)



