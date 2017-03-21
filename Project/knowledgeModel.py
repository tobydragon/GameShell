__author__ = 'Kevin Pomer'
class KnowledgeModel:
    def __init__(self):
        self.individualKnowledgeScore = {}

        self.tagKnowledgeScore = {}

    def updateIndividualScore(self, name, score):
        if name in self.individualKnowledgeScore:
            self.individualKnowledgeScore[name].append(score)

        else:
            self.individualKnowledgeScore[name] = [score]


    def checkCorrectCards(self, correct, incorrect, right, wrong, scoreInfo):
        rightVal = round(100*scoreInfo.rightVal,1)
        wrongVal = round(100*scoreInfo.wrongVal,1)

        individualScores = {}

        for card in correct:
            name = str(card.individual)
            name = name.split("_")
            name = name[1]
            if card in right:
                individualScores[name] = rightVal
            elif card in wrong:
                individualScores[name] = wrongVal

        for card in incorrect:
            name = str(card.individual)
            name = name.split("_")
            name = name[1]
            if card in right:
                individualScores[name] = rightVal * -1
            elif card in wrong:
                individualScores[name] = wrongVal * -1

        for individual in individualScores:
            self.updateIndividualScore(individual, individualScores[individual])

    def updateTagScore(self, tag, score):
        if tag in self.tagKnowledgeScore:
            self.tagKnowledgeScore[tag].append(score)
            #This must be fixed because it is a percent so adding score will make it >100%
            #TODO: Create a method of updating the tag score based on percentage rather than adding them together

        else:
            self.tagKnowledgeScore[tag] = [score]


    def getIndividualScore(self, keyToGet):
        #TODO: use scoreTimeStampModel.py to change the amount different scores matter to total score
        if keyToGet in self.individualKnowledgeScore:
            totalScore = 0
            for score in self.individualKnowledgeScore[keyToGet]:
                totalScore = totalScore + score

            totalScore = totalScore/len(self.individualKnowledgeScore[keyToGet])
            return totalScore

        else:
            # Should this return anything?
            print("There is no score for this key")

    def getTagScore(self, keyToGet):
        # TODO: use scoreTimeStampModel.py to change the amount different scores matter to total score
        if keyToGet in self.tagKnowledgeScore:
            totalScore = 0
            for score in self.tagKnowledgeScore[keyToGet]:
                totalScore = totalScore + score

            totalScore = totalScore / len(self.tagKnowledgeScore[keyToGet])
            return totalScore

        else:
            #Should this return anything?
            print("There is no score for this key")
