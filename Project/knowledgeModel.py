__author__ = 'Kevin Pomer'
class KnowledgeModel:
    def __init__(self):
        self.individualKnowledgeScore = {}
        self.num_Individuals = 0

        self.tagKnowledgeScore = {}
        self.num_Tags = 0

    def updateIndividualScore(self, name, score):
        if name in self.individualKnowledgeScore:
            self.individualKnowledgeScore[name] = self.individualKnowledgeScore[name] + score

        else:
            self.individualKnowledgeScore[name] = []
            self.num_Individuals = self.num_Individuals + 1

    def checkCorrectCards(self, cardList):
        for i in range(len(cardList)):
            checkCorrect = cardList[i].symbol
            if (checkCorrect == 2):
                #Correct
                self.updateIndividualScore(cardList[i].individual.name, 1)

            elif (checkCorrect == 3):
                #Incorrect
                self.updateIndividualScore(cardList[i].individual.name, -1)

            else:
                print("Error, card symbol (correct or incorrect) did not return value of 2 or 3")

        # Card SCORE PRINTOUT (Must Create function)
        # self.printCards()



    def updateTagScore(self, tag, score):
        if tag in self.tagKnowledgeScore:
            self.tagKnowledgeScore[tag] = self.tagKnowledgeScore[tag] + score
            #This must be fixed because it is a percent so adding score will make it >100%
            #TODO: Create a method of updating the tag score based on percentage rather than adding them together

        else:
            self.tagKnowledgeScore[tag] = score
            self.num_Tags = self.num_Tags + 1

        #TAG SCORE PRINTOUT (Must Create function)
        #self.printTags()

    def getCardScore(self, keyToGet):
        if keyToGet in self.individualKnowledgeScore:
            print("Key: ", keyToGet, " Score: ", self.individualKnowledgeScore[keyToGet])
            return self.individualKnowledgeScore[keyToGet]

        else:
            print("There is no score for this key")

    def getTagScore(self, keyToGet):
        if keyToGet in self.tagKnowledgeScore:
            print("Key: ", keyToGet, " Score: ", self.tagKnowledgeScore[keyToGet])
            return self.tagKnowledgeScore[keyToGet]

        else:
            print("There is no score for this key")
