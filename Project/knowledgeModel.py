__author__ = 'Kevin Pomer'
import assessmentEventModel



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


            ##Settings from selected settings file
            self.timeStamp_Window = settings.getTimeStampWindow()
            self.tagCompetentThreshold = settings.getTagCompetentThreshold()
            self.tagIncompetentThreshold = settings.getTagIncompetentThreshold()
            self.individualCompetentThreshold = settings.getIndividualCompetentThreshold()
            self.individualIncompetentThreshold = settings.getIndividualIncompetentThreshold()
            self.computeScore = settings.getComputeScore()

    ##BEGIN INDIVIDUAL METHODS##
    def updateIndividualScore(self, individualScores):
        for individual in individualScores:
            event = assessmentEventModel.AssesmentEvent(individualScores[individual])
            if individual in self.individualKnowledgeScore:
                self.individualKnowledgeScore[individual].append(event)

            else:
                self.individualKnowledgeScore[individual] = [event]

      ###PRINTOUT FOR PLAYTESTING###
        print("\nKnowledgeModel Individual Scores Updated:")
        for ind in self.individualKnowledgeScore:
            print(ind, "\tTOTAL: ", self.calcIndividualScore(ind))

            for event in self.individualKnowledgeScore[ind]:
                print("\tTimeStamp: ", event.getTime(), "\tScore: ", event.getScore())
      ###PRINTOUT FOR PLAYTESTING###

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
        totalScore = self.computeScore(self.individualKnowledgeScore[keyToGet])
        return totalScore

    def updateIndividualBuckets(self):
        for ind in self.individualBuckets["Not Asked"]:
            if ind in self.individualKnowledgeScore:
                self.individualBuckets["Unclear"].append(ind)

        for ind in self.individualKnowledgeScore:
            if ind in self.individualBuckets["Not Asked"]:
                self.individualBuckets["Not Asked"].remove(ind)



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

                ###PRINTOUT FOR PLAYTESTING###
            print("\nKnowledgeModel Individual Buckets Updated: ")  ###Printout
            print("\tCompetent: ", self.individualBuckets["Competent"])  ###Printout
            print("\tIncompetent: ", self.individualBuckets["Incompetent"])  ###Printout
            print("\tUnclear: ", self.individualBuckets["Unclear"])  ###Printout
            print("\tNot Asked: ", self.individualBuckets["Not Asked"])  ###Printout
            ###PRINTOUT FOR PLAYTESTING###

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

  ###PRINTOUT FOR PLAYTESTING###
        print("\nKnowledgeModel Tag Score Updated:")
        for tag in self.questionTagKnowledgeScore:
            print(tag, "\tTOTAL: ", self.calcQuestionTagScore(tag))
            for event in self.questionTagKnowledgeScore[tag]:
                print("\tTimeStamp: ", event.getTime(), "\tScore: ", event.getScore())

        print("\nKnowledgeModel TagType Score Updated: ")
        for tagType in self.questionTagTypeDictionary:
            print("\t", tagType, ": ", self.calcQuestionTagTypeScore(tagType))
  ###PRINTOUT FOR PLAYTESTING###


    def calcQuestionTagScore(self, keyToGet):
        # TODO: use scoreTimeStampModel.py to change the amount different scores matter to total score
        if keyToGet not in self.questionTagKnowledgeScore:
            totalScore = 0
        else:
            totalScore = self.computeScore(self.questionTagKnowledgeScore[keyToGet])
        return totalScore

        ###PRINTOUT FOR PLAYTESTING###
        print("\nKnowledgeModel Tag Buckets Updated: ")  ###Printout
        print("\tCompetent: ", self.tagBuckets["Competent"])  ###Printout
        print("\tIncompetent: ", self.tagBuckets["Incompetent"])  ###Printout
        print("\tUnclear: ", self.tagBuckets["Unclear"])  ###Printout
        print("\tNot Asked: ", self.tagBuckets["Not Asked"])  ###Printout
        ###PRINTOUT FOR PLAYTESTING###

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
