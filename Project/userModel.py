__author__ = 'JoãoGabriel'
class User:
    def __init__(self, username="NO_USER", json=None):
        """
        NOTE: JSON data overrides input and default data
        :param username: username
        :param json: json data to load from
        """
        #TODO remove rightAnswers and wrongsxAnswers
        self.username = username
        self.score = 0
        self.percentages=[]
        self.currentStage = 1
        if json:
            self.fromJSON(json)

    def getAveragePercent(self):
        try:
            return sum(self.percentages)/float(len(self.percentages))
        except ZeroDivisionError as e:
            return 0

    def addPercent(self,percent):
        self.percentages.append(percent)

    def __repr__(self):
        return("Name: " + self.username + "\n" +
               "Score: " + str(self.score) +"\n" +
               "Current Stage: " + str(self.currentStage) +"\n")

    def toJSON(self):
        base = {}
        base["username"] = self.username
        base["score"] = self.score
        base["percentages"]=self.percentages
        base["currentStage"] = self.currentStage
        return base

    def fromJSON(self, json):
        try:
            self.username = json["username"]
            self.currentStage = json["currentStage"]
            self.score = json["score"]
            self.percentages = json["percentages"]
        except KeyError as e:
            print(e)