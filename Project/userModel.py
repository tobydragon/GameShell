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
        self.currentStage = 1
        self.rightAnswers = []
        self.wrongAnswers = []
        if json:
            self.fromJSON(json)

    #TODO remove
    def retrieveData(self, userData):
        scoreLine = userData[0] #Line with the Score
        divide = scoreLine.split(": ")
        self.score = int(divide[1]) #Number, after the ": "

        stageLine = userData[1] #Line with the Current Stage
        divide = stageLine.split(": ")
        self.currentStage = int(divide[1]) #Number, after the ": "

        self.rightAnswers = []
        singleAnswer = ""
        open = False
        for char in userData[2]: #Line with the Right Answers
            if char != "'" and open:
                singleAnswer += char

            if char == "'" and not open:
                open = True
            elif char == "'" and open:
                open = False
                self.rightAnswers.append(str(singleAnswer))
                singleAnswer = ""

        self.wrongAnswers = [] #Line with the Wrong Answers
        singleAnswer = ""
        open = False
        for char in userData[3]: #Line with the Right Answers
            if char != "'" and open:
                singleAnswer += char

            if char == "'" and not open:
                open = True
            elif char == "'" and open:
                open = False
                self.wrongAnswers.append(str(singleAnswer))
                singleAnswer = ""


    def __repr__(self):
        return("Name: " + self.username + "\n" +
               "Score: " + str(self.score) +"\n" +
               "Current Stage: " + str(self.currentStage) +"\n" +
               "Right Answers: " + str(self.rightAnswers) +"\n" +
               "Wrong Answers: " + str(self.wrongAnswers) +"\n")

    def toJSON(self):
        base = {}
        base["username"] = self.username
        base["score"] = self.score
        base["currentStage"] = self.currentStage
        return base

    def fromJSON(self, json):
        try:
            self.username = json["username"]
            self.currentStage = json["currentStage"]
            self.score = json["score"]
        except KeyError as e:
            print(e)