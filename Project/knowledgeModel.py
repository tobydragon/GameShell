__author__ = 'Kevin Pomer'
class Knowledge:
    def __init__(self):
        ##Will we want to take values from a json file
        ##such as the tags or the insect names?
        self.knowledgeScore = {}

    def addKey(self, newKey):
        self.knowledgeScore[newKey] = 0
        ##we may want to pass a starting score rather than 0

    def updateScore(self, keyToUpdate, newScore):
        self.knowledgeScore[keyToUpdate] = newScore
        #is it necessary to check to see if key already exists?

    def getScore(self, keyToGet):
        if keyToGet in self.knowledgeScore:
            return self.knowledgeScore[keyToGet]

        else:
            print("There is no score for this key")
