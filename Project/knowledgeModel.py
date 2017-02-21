__author__ = 'Kevin Pomer'
class KnowledgeModel:
    def __init__(self):
        self.individualKnowledgeScore = {}
        self.num_Individuals = 0

        self.tagKnowledgeScore = {}
        self.num_Tags = 0

    #individuals is list of individuals on stage
    #scores are corresponding score (correct = 1) (incorrect = -1)
    #length is number of values in lists indiviuals and scores
    def updateIndividualScore(self, individuals, scores, length):
        print("Test")
        for i in length:
            if individuals[i] in self.individualKnowledgeScore:
                self.individualKnowledgeScore[individuals[i]] = self.individualKnowledgeScore[individuals[i]] + scores[i]

            else:
                self.individualKnowledgeScore[individuals[i]] = scores[i]
                self.num_Individuals = self.num_Individuals + 1

        for z in self.individualKnowledgeScore:
            print(z, ": ", self.individualKnowledgeScore[z])

    def updateTagScore(self, tag, score):
        if tag in self.tagKnowledgeScore:
            self.tagKnowledgeScore[tag] = self.tagKnowledgeScore[tag] + score
            #This must be fixed because it is a percent so adding score will make it >100%

        else:
            self.tagKnowledgeScore[tag] = score
            self.num_Tags = self.num_Tags + 1

    def getIndividualScore(self, keyToGet):
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