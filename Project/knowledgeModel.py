__author__ = 'Kevin Pomer'
import assessmentEventModel
from stageController import CardStateInfo


class KnowledgeModel:
    def __init__(self, qTagTypeDict, individualList, settings, json=None):
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

            self.individualBuckets = {"Competent": [], "Incompetent": [], "Unclear": [], "Not Asked": individuals}
            #Competent = ##High Score
            #InCompetent = #Low Score
            #Unclear = ##Score unclear (not high or low) after asking questions
            #Not Asked = ##Not questioned yet

            self.questionTagTypeDictionary = qTagTypeDict  ##ORiginally from domainModel.py --> {questionTagType:[questionTags]}

            tagList = [] ##List of all tags
            for tagType in self.questionTagTypeDictionary:
                for tag in self.questionTagTypeDictionary[tagType]:
                    tagList.append(tag)

            # Buckets of tags to understand user's knowledge of tag after asking questions
            self.tagBuckets = {"Competent": [], "Incompetent": [], "Unclear": [], "Not Asked": tagList}
            # Competent = ##High Score
            # InCompetent = #Low Score
            # Unclear = ##Score unclear (not high or low) after asking questions
            # Not Asked = ##Not questioned yet

            self.timeStamp_Window = settings.getTimeStampWindow()
            self.tagCompetentThreshold = settings.getTagCompetentThreshold()
            self.tagIncompetentThreshold = settings.getTagIncompetentThreshold()
            self.individualCompetentThreshold = settings.getIndividualCompetentThreshold()
            self.individualIncompetentThreshold = settings.getIndividualIncompetentThreshold()


    ##BEGIN INDIVIDUAL METHODS##
    def updateIndividualScore(self, individualScores):
        for individual in individualScores:
            event = assessmentEventModel.AssesmentEvent(individualScores[individual])
            if individual in self.individualKnowledgeScore:
                self.individualKnowledgeScore[individual].append(event)

            else:
                self.individualKnowledgeScore[individual] = [event]



    def checkCorrectCards(self, cardResults, scoreInfo):
        ##Used to calculate Individual Score

        individualScores = {}

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

        for ind in self.individualBuckets["Unclear"]:  # Should this check Competent and Incompetent buckets too?
            if len(self.individualKnowledgeScore[ind]) >= self.timeStamp_Window:
                score = 0
                events = self.individualKnowledgeScore[ind]
                for e in events:
                    score = score + e.getScore()


                if score >= self.individualCompetentThreshold:
                    self.individualBuckets["Competent"].append(ind)
                    self.individualBuckets["Unclear"].remove(ind)

                if score <= self.individualIncompetentThreshold:
                    self.individualBuckets["Incompetent"].append(ind)
                    self.individualBuckets["Unclear"].remove(ind)

    def getIndividualBuckets(self):
        return self.individualBuckets

    ##END INDIVIDUAL METHODS##

    ##BEGIN QUESTION_TAG METHODS##
    def updateQuestionTagScore(self, tag, score):
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

        for tag in self.tagBuckets["Unclear"]:  #Should this check Competent and Incompetent buckets too?
            if len(self.questionTagKnowledgeScore[tag]) >= self.timeStamp_Window:
                score = 0
                events = self.questionTagKnowledgeScore[tag]
                for e in events:
                    score = score + e.getScore()
                score = score/(len(events))

                if score >= self.tagCompetentThreshold:
                    self.tagBuckets["Competent"].append(tag)
                    self.tagBuckets["Unclear"].remove(tag)

                if score <= self.tagIncompetentThreshold:
                    self.tagBuckets["Incompetent"].append(tag)
                    self.tagBuckets["Unclear"].remove(tag)

    def getTagBuckets(self):
        return self.tagBuckets
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
    totalScore = 0
    if len(events) == 0:
        return 0 ##Must be 0 for calcQuestionTagTypeScore()
    else:
        for i in events:
            score = i.getScore()
            totalScore = totalScore + score

    totalScore = totalScore/(len(events))
    return totalScore