from unittest import TestCase

from knowledgeModel import KnowledgeModel

class TestKnowledgeScore(TestCase):

    def testTagScore(self):
        testKnowledge = KnowledgeModel()
        testKnowledge.updateTagScore("tag1", 0.5)
        self.assertEqual(0.5, testKnowledge.getTagScore("tag1"))
        testKnowledge.updateTagScore("tag1", 0.75)
        self.assertEqual(0.625, testKnowledge.getTagScore("tag1"))

    def testIndividualScore(self):
        #Does not use timeStamp, but instead averages all scores
        testKnowledge = KnowledgeModel()
        testKnowledge.updateIndividualScore("i1", 5.6)
        testKnowledge.updateIndividualScore("i2", 7)
        testKnowledge.updateIndividualScore("i3", -4)
        testKnowledge.updateIndividualScore("i4", 50)
        testKnowledge.updateIndividualScore("i5", 0)
        self.assertEqual(5.6, testKnowledge.getIndividualScore("i1"))
        self.assertEqual(-4, testKnowledge.getIndividualScore("i3"))
        testKnowledge.updateIndividualScore("i3", -5)
        testKnowledge.updateIndividualScore("i1", -4.5)
        testKnowledge.updateIndividualScore("i2", 0)
        self.assertEqual(-4.5, testKnowledge.getIndividualScore("i3"))
        self.assertEqual(0.55, testKnowledge.getIndividualScore("i1")) ##This is not a fail, how can I fix this?
        self.assertEqual(3.5, testKnowledge.getIndividualScore("i2"))