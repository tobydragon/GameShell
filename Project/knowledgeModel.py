__author__ = 'Kevin Pomer'
import assessmentEventModel
from stageController import CardStateInfo


class KnowledgeModel:
    def __init__(self, qTagTypeDict, json=None):
        if json:
            self.fromJSON(json)

        else:
            self.individualKnowledgeScore = {}
            self.questionTagKnowledgeScore = {}

        self.questionTagTypeDictionary = qTagTypeDict ##ORiginally from domainModel.py --> {questionTagType:[questionTags]}

    ##BEGIN INDIVIDUAL METHODS##
    def updateIndividualScore(self, name, score, difficulty):
        event = assessmentEventModel.AssesmentEvent(score, difficulty)
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
        ##Used to calculate Individual Score
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

    def calcIndividualScore(self, keyToGet):
        #TODO: use scoreTimeStampModel.py to change the amount different scores matter to total score
        totalScore = computeScore(self.individualKnowledgeScore[keyToGet])
        return totalScore
    ##END INDIVIDUAL METHODS##

    ##BEGIN QUESTION_TAG METHODS##
    def calcQuestionTagDifficulty(self, cardResults):
        #Current system is based on number of correct answers in question
        #This can be changed in the future when a better method is decided on
        #Scored 1 - 10
        numCorrect = len(cardResults.correct)

        if (numCorrect == 0):
            difficulty = 10

        else:
            difficulty = 11 - numCorrect ##more correct = easier

        return difficulty

    def updateQuestionTagScore(self, tag, score, cardResults):
        difficulty = self.calcQuestionTagDifficulty(cardResults)
        event = assessmentEventModel.AssesmentEvent(score, difficulty)
        if tag in self.questionTagKnowledgeScore:
            self.questionTagKnowledgeScore[tag].append(event)
            #TODO: Create a method of updating the tag score based on percentage rather than adding them together

        else:
            self.questionTagKnowledgeScore[tag] = [event]


    def calcQuestionTagScore(self, keyToGet):
        # TODO: use scoreTimeStampModel.py to change the amount different scores matter to total score
        if keyToGet not in self.questionTagKnowledgeScore:
            totalScore = 0
        else:
            totalScore = computeScore(self.questionTagKnowledgeScore[keyToGet])
        return totalScore

    ##END QUESTION_TAG METHODS##


    ##BEGIN_QUESTION_TAG_TYPE_METHODS##

    def calcQuestionTagTypeScore(self, tagTypeToGet):
        ##Uses the scores from each questionTag within a questionTagType to calculate a questionTagType score
        score = 0
        numTags = 0
        if tagTypeToGet in self.questionTagTypeDictionary:
            listOfTags = self.questionTagTypeDictionary[tagTypeToGet]
            numTags = len(listOfTags)
            for tag in listOfTags:

                tagScore = self.calcQuestionTagScore(tag)
                score = score + tagScore
        else:
            print(tagTypeToGet, " is not one of the tagTypes asked about.")

        score = score/numTags
        return score
        ##Average of the tag scores for each tagType

    ##END_QUESTION_TAG_TYPE_METHODS##


    #TODO: Create method to calculate questionTagTypeKnowledgeScore from values in dict questionTagKnowledgeScore

    def toJSON(self):
        base = {}
        base["individualKnowledgeScore"] = self.individualKnowledgeScore
        base["questionTagKnowledgeScore"] = self.questionTagKnowledgeScore

        return base

    def fromJSON(self, json):
        try:
            self.individualKnowledgeScore = json["individualKnowledgeScore"]
            self.questionTagKnowledgeScore = json["questionTagKnowledgeScore"]

        except KeyError as e:
            print(e)

#must import knowledgeModel to call
from knowledgeModel import KnowledgeModel
from assessmentEventModel import AssesmentEvent
def computeScore(events):
    difficulties = []
    totalScore = 0
    if len(events) == 0:
        return 0 ##Must be 0 for calcQuestionTagTypeScore()
    else:
        for i in events:
            diff = i.getDifficulty()
            score = i.getScore()
            totalScore = totalScore + (diff*score)
            difficulties.append(i.getDifficulty())

        averageDifficulty = 0
        for d in difficulties:
            averageDifficulty = averageDifficulty + d

        averageDifficulty = averageDifficulty/(len(difficulties))

        totalScore = totalScore/(len(events)*averageDifficulty)
        return totalScore