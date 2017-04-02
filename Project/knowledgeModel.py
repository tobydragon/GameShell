__author__ = 'Kevin Pomer'
import scoreTimestampModel
from stageController import CardStateInfo

class KnowledgeModel:
    def __init__(self):
        self.individualKnowledgeScore = {}
        self.tagKnowledgeScore = {}

    def updateIndividualScore(self, name, score, difficulty):
        event = scoreTimestampModel.AssesmentEvent(score, difficulty)
        if name in self.individualKnowledgeScore:
            self.individualKnowledgeScore[name].append(event)

        else:
            self.individualKnowledgeScore[name] = [event]

    def calcIndividualDifficulty(self, cardResults):
        ##This should be changed when a better method is created to set difficulty
        difficulty = {}

        for card in cardResults.rightTag:
            name = str(card.individual)
            name = name.split("_")
            name = name[1]

            if card in cardResults.selected:
                difficulty[name] = 2 #rightTag selected = easiest

            else:
                difficulty[name] = 4 #rightTag unselected = medium low difficulty

        for card in cardResults.wrongTag:
            name = str(card.individual)
            name = name.split("_")
            name = name[1]

            if card in cardResults.unselected:
                difficulty[name] = 6 #wrongTag unselected = medium high difficulty

            else:
                difficulty[name] = 8 #wrongTag selected = high difficulty

        return difficulty


    def checkCorrectCards(self, cardResults, scoreInfo):
        rightVal = round(100*scoreInfo.rightVal,1)
        wrongVal = round(100*scoreInfo.wrongVal,1)

        individualScores = {}

        difficulty = self.calcIndividualDifficulty(cardResults)

        for card in cardResults.correct:
            name = str(card.individual)
            name = name.split("_")
            name = name[1]
            if card in cardResults.rightTag:
                individualScores[name] = rightVal
            elif card in cardResults.wrongTag:
                individualScores[name] = wrongVal

        for card in cardResults.incorrect:
            name = str(card.individual)
            name = name.split("_")
            name = name[1]
            if card in cardResults.rightTag:
                individualScores[name] = rightVal * -1
            elif card in cardResults.wrongTag:
                individualScores[name] = wrongVal * -1


        for individual in individualScores:
            self.updateIndividualScore(individual, individualScores[individual], difficulty[individual])

    def getTagDifficulty(self, cardResults):
        #Current system is based on number of correct answers in question
        #This can be changed in the future when a better method is decided on
        #Scored 1 - 10
        numCorrect = len(cardResults.correct)

        if (numCorrect == 0):
            difficulty = 10

        else:
            difficulty = 11 - numCorrect ##more correct = easier

        return difficulty

    def updateTagScore(self, tag, score, cardResults):
        difficulty = self.getTagDifficulty(cardResults)
        event = scoreTimestampModel.AssesmentEvent(score, difficulty)
        if tag in self.tagKnowledgeScore:
            self.tagKnowledgeScore[tag].append(event)
            #TODO: Create a method of updating the tag score based on percentage rather than adding them together

        else:
            self.tagKnowledgeScore[tag] = [event]


    def calcIndividualScore(self, keyToGet):
        #TODO: use scoreTimeStampModel.py to change the amount different scores matter to total score
        totalScore = computeScore(self.individualKnowledgeScore[keyToGet])
        return totalScore


        """
        Old method of doing score


        :param keyToGet:
        :return:

        if keyToGet in self.individualKnowledgeScore:
            totalScore = 0
            for score in self.individualKnowledgeScore[keyToGet]:
                totalScore = totalScore + score

            totalScore = totalScore/len(self.individualKnowledgeScore[keyToGet])
            return totalScore

        else:
            # Should this return anything?
            print("There is no score for this key")
        """

    def calcTagScore(self, keyToGet):
        # TODO: use scoreTimeStampModel.py to change the amount different scores matter to total score
        totalScore = computeScore(self.TagScore[keyToGet])
        return totalScore


        """
        Old method of scoring


        :param keyToGet:
        :return:

        if keyToGet in self.tagKnowledgeScore:
            totalScore = 0
            for timeStamp in self.tagKnowledgeScore[keyToGet]:
                totalScore = totalScore + timeStamp.getScore()

            totalScore = totalScore / len(self.tagKnowledgeScore[keyToGet])
            return totalScore

        else:
            #Should this return anything?
            print("There is no score for this key")
        """

#must import knowledgeModel to call
from knowledgeModel import KnowledgeModel
from scoreTimestampModel import AssesmentEvent
def computeScore(events):
    difficulties = []
    totalScore = 0

    for i in events:
        diff = i.getDifficulty
        score = i.getScore
        print(diff)
        totalScore = totalScore + (diff*score)
        difficulties.append(i.getDifficulty)

    averageDifficulty = 0
    for d in difficulties:
        averageDifficulty = averageDifficulty + d

    averageDifficulty = averageDifficulty/len(averageDifficulty)

    totalScore = totalScore/(len(events)*averageDifficulty)
    return totalScore
