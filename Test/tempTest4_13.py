from unittest import TestCase
#from stageController import CardStateInfo

class TestCardStateInfo(TestCase):


    def buildExampleIntCardState(self):
        selected=[1, 2, 3, 4]
        unselected=[5, 6, 7, 8]
        rightTag=[1, 2, 5, 6]
        wrongTag=[3, 4, 7, 8]
        #return CardStateInfo(selected, unselected, rightTag, wrongTag)

    def testConstructor(self):
        intCardStateInfo = self.buildExampleIntCardState()

        self.assertEqual([5, 5], [5, 5])

        ##self.assertCountEqual([1,2], intCardStateInfo.correctRightTag)
        ##self.assertCountEqual([7, 8], intCardStateInfo.correctWrongTag)
        ##self.assertCountEqual([1, 2, 7, 8], intCardStateInfo.correct)
        ##self.assertCountEqual([3, 4, 5, 6], intCardStateInfo.incorrect)
