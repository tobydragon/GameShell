__author__ = 'Kevin Pomer'
import assessmentEventModel
from stageController import CardStateInfo


class KnowledgeModel:
    def __init__(self, qTagTypeDict, individualList, json=None):
        if json:
            self.fromJSON(json)

        else:
            self.individualKnowledgeScore = {}
            self.questionTagKnowledgeScore = {}

            #Buckets of individuals to understand user's knowledge of individual after asking questions
            individuals = []
            for ind in individualList: ##GEt string names for individuals
                name = str(ind)
                name = name.split("_")
                name = name[1]
                individuals.append(name)

            self.individualBuckets = {"Known": [], "Unknown": [], "Unclear": [], "Not Asked": individuals}
            #Known = ##High Score
            #Unknown = #Low Score
            #Unclear = ##Score unclear (not high or low) after asking questions
            #Not Asked = ##Not questioned yet

            self.questionTagTypeDictionary = qTagTypeDict  ##ORiginally from domainModel.py --> {questionTagType:[questionTags]}

            tagList = [] ##List of all tags
            for tagType in self.questionTagTypeDictionary:
                for tag in self.questionTagTypeDictionary[tagType]:
                    tagList.append(tag)

            # Buckets of tags to understand user's knowledge of tag after asking questions
            self.tagBuckets = {"Known": [], "Unknown": [], "Unclear": [], "Not Asked": tagList}
            # Known = ##High Score
            # Unknown = #Low Score
            # Unclear = ##Score unclear (not high or low) after asking questions
            # Not Asked = ##Not questioned yet


    ##BEGIN INDIVIDUAL METHODS##
    def updateIndividualScore(self, individualScores):
        for individual in individualScores:
            event = assessmentEventModel.AssesmentEvent(individualScores[individual])
            if individual in self.individualKnowledgeScore:
                self.individualKnowledgeScore[individual].append(event)

            else:
                self.individualKnowledgeScore[individual] = [event]


    def calcIndividualDifficulty(self, cardResults):
        ##This should be changed when a better method is created to set difficulty
  #      difficulty = {}

   #     for card in cardResults.rightTag:
    #        name = str(card.individual)
#            name = name.split("_")
 #           name = name[1]

  #          if card in cardResults.selected:
   #             difficulty[name] = 2 #rightTag selected = easiest

    #        else:
     #           difficulty[name] = 4 #rightTag unselected = medium low difficulty

      #  for card in cardResults.wrongTag:
       #     name = str(card.individual)
        #    name = name.split("_")
         #   name = name[1]

#            if card in cardResults.unselected:
 #               difficulty[name] = 6 #wrongTag unselected = medium high difficulty
#
 #           else:
  #              difficulty[name] = 8 #wrongTag selected = high difficulty

#        return difficulty
        return 0 #Not using this function


    def checkCorrectCards(self, cardResults, scoreInfo):
        ##Used to calculate Individual Score

        individualScores = {}

        #difficulty = self.calcIndividualDifficulty(cardResults)

        for card in cardResults.correct:
            name = str(card.individual)
            name = name.split("_")
            name = name[1]
            if card in cardResults.rightTag:
                individualScores[name] = 1
            elif card in cardResults.wrongTag:
                individualScores[name] = 1

        for card in cardResults.incorrect:
            name = str(card.individual)
            name = name.split("_")
            name = name[1]
            if card in cardResults.rightTag:
                individualScores[name] = -1
            elif card in cardResults.wrongTag:
                individualScores[name] = -1


        self.updateIndividualScore(individualScores)

    def calcIndividualScore(self, keyToGet):
        #TODO: use scoreTimeStampModel.py to change the amount different scores matter to total score
        totalScore = computeScore(self.individualKnowledgeScore[keyToGet])
        return totalScore

    def updateIndividualBuckets(self):
        print("Not Asked", self.individualBuckets["Not Asked"]) ##DELETE
        print("Unclear", self.individualBuckets["Unclear"]) ##DELETE
        print(len(self.individualBuckets["Not Asked"])) ##DELETE
        for ind in self.individualBuckets["Not Asked"]:
            print(ind)  ##WHY ARE SOME MISSING??? ##DELETE
            print(len(self.individualBuckets["Not Asked"]))  ##DELETE
            if ind in self.individualKnowledgeScore:
                print("HAS K_SCORE: ", ind) ##DELETE
                self.individualBuckets["Unclear"].append(ind)
                print("Ind To Remove: ", ind)  ##DELETE
                self.individualBuckets["Not Asked"].remove(ind)
                print("Ind Removed: ", ind) ##DELETE

        print("Not Asked", self.individualBuckets["Not Asked"]) ##DELETE
        print("Unclear", self.individualBuckets["Unclear"]) ##DELETE

        for ind in self.individualBuckets["Unclear"]:  # Should this check Known and Unknown buckets too?
            if len(self.individualKnowledgeScore[ind]) >= 10:
                score = 0
                events = self.individualKnowledgeScore[ind]
                for e in events:
                    score = score + e.getScore()
                score = score / (len(events))

                if score >= 6:
                    self.individualBuckets["Known"].append(ind)
                    self.individualBuckets["Unclear"].remove(ind)

                if score <= -6:
                    self.individualBuckets["Unknown"].append(ind)
                    self.individualBuckets["Unclear"].remove(ind)
    ##END INDIVIDUAL METHODS##

    ##BEGIN QUESTION_TAG METHODS##
    def calcQuestionTagDifficulty(self, cardResults):
        #Current system is based on number of correct answers in question
        #This can be changed in the future when a better method is decided on
        #Scored 1 - 10

 #       numCorrect = len(cardResults.correct)

  #      if (numCorrect == 0):
   #         difficulty = 10

    #    else:
     #       difficulty = 11 - numCorrect ##more correct = easier

      #  return difficulty
        return 0  # Not using this function

    def updateQuestionTagScore(self, tag, score):
        #difficulty = self.calcQuestionTagDifficulty(cardResults)
        event = assessmentEventModel.AssesmentEvent(score)
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

    def updateTagBuckets(self):
        for tag in self.tagBuckets["Not Asked"]:
            if tag in self.questionTagKnowledgeScore:
                self.tagBuckets["Unclear"].append(tag)
                self.tagBuckets["Not Asked"].remove(tag)

        for tag in self.tagBuckets["Unclear"]:  #Should this check Known and Unknown buckets too?
            if len(self.questionTagKnowledgeScore[tag]) >= 10:
                score = 0
                events = self.questionTagKnowledgeScore[tag]
                for e in events:
                    score = score + e.getScore()
                score = score/(len(events))

                if score >= 0.8:
                    self.tagBuckets["Known"].append(tag)
                    self.tagBuckets["Unclear"].remove(tag)

                if score <= 0.2:
                    self.tagBuckets["Unknown"].append(tag)
                    self.tagBuckets["Unclear"].remove(tag)

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
        base["tagBuckets"] = self.tagBuckets
        base["individualBuckets"] = self.individualBuckets

        return base

    def fromJSON(self, json):
        try:
            self.individualKnowledgeScore = json["individualKnowledgeScore"]
            self.questionTagKnowledgeScore = json["questionTagKnowledgeScore"]
            self.tagBuckets = json["tagBuckets"]
            self.individualBuckets = json["individualBuckets"]

        except KeyError as e:
            print(e)

#must import knowledgeModel to call
from knowledgeModel import KnowledgeModel
from assessmentEventModel import AssesmentEvent
def computeScore(events):
#    difficulties = []
#   totalScore = 0
#    if len(events) == 0:
#        return 0 ##Must be 0 for calcQuestionTagTypeScore()
#    else:
#        for i in events:
#            diff = i.getDifficulty()
#            score = i.getScore()
#            totalScore = totalScore + (diff*score)
#            difficulties.append(i.getDifficulty())

#        averageDifficulty = 0
#        for d in difficulties:
#            averageDifficulty = averageDifficulty + d

#        averageDifficulty = averageDifficulty/(len(difficulties))

 #       totalScore = totalScore/(len(events)*averageDifficulty)
  #      return totalScore
    return 0  # Not using this function