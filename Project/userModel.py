__author__ = 'JoãoGabriel'
class User:
    def __init__(self, name, userData = None):
        self.name = name
        if(userData == None):
            self.score = 0
            self.currentStage = 1
        else:
            self.score = int(userData[0])
            self.currentStage = int(userData[1])
        self.rightAnswers = []
        self.wrongAnswers = []