import domainModel, random, pygame, sys, stageView, gameView, stageModel, userModel, startMenu, os.path, jsonIO
from pygame.locals import *

WINDOWWIDTH = 1500
WINDOWHEIGHT = 850
DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
USER_DATA_DIR = "userdata/"

class Controller:
    def __init__(self, domModel, userName):
        self.FPS = 30
        self.fpsClock = pygame.time.Clock()
        self.domainModel = domModel
        #self.userName = userName
        self.game = False

        # No name represents debugging; no saves are made
        if userName != "" and os.path.isfile(USER_DATA_DIR+userName): #Check if there is already a file for this User
            try:
                self.fromJSON(jsonIO.loadFromJson(USER_DATA_DIR + userName))
            # TODO handle this better
            except BaseException as e:
                print("Unable to load save. Error:\n\t", e)
                self.user = userModel.User(userName)
                self.stageModel = stageModel.StageModel(domModel)
        else:
            self.user = userModel.User(userName)
            self.stageModel = stageModel.StageModel(domModel)

        self.startMenu = startMenu.StartMenu(DISPLAYSURFACE, self.user.username)
        self.stageView = stageView.StageView(self.stageModel, 100, 50, DISPLAYSURFACE)
        self.gameView = gameView.GameView(DISPLAYSURFACE)
        self.showNextButton = False


    """
    def readFile(self):
        fileInput = open(USER_DATA_DIR+self.userName, "r")
        lines = fileInput.readlines()
        self.user = userModel.User(self.userName, lines[1:5]) #Passing lines (Score, Current Stage,  Right & Wrong Answers)
        self.stageModel = stageModel.StageModel(self.domainModel, lines[5], lines[6]) #Passing lines (Current Stage Category & Animals)


    def writeFile(self):
        #No name represents debugging; no saves are made
        if self.user.username == "":
            return
        file = open(USER_DATA_DIR + self.user.username, "w")
        file.truncate() #Clear file
        file.write(self.user.__repr__()) #Write Student Information
        file.write(self.stageModel.__repr__()) #Write Current Stage Information, for Loading PS: The last played answers will be in the end between []
        file.close()
"""

    def gameLoop(self):

        while True:
            if self.game: #After clicking START (After Start Menu Screen)
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        jsonIO.saveToJson(USER_DATA_DIR+self.user.username,self)
                        pygame.quit()
                        sys.exit()
                    ###
                    if self.showNextButton:
                        buttonResponse = self.gameView.checkForNextButton(event)
                        if buttonResponse or (event.type == KEYDOWN and event.key == K_RETURN):
                            self.nextStage()

                    else:
                        self.checkCards(event)
                    ###
                    """
                    #Correct, Incorrect or "Already clicked"(null) decision
                    buttonResponse = self.stageView.checkForButtonClick(event, self.showNextButton)
                    if buttonResponse != None:
                        pass
                        # if buttonResponse != None and buttonResponse != "null" and buttonResponse != "correct":
                        #     pygame.mixer.music.load('sounds/incorrect.mp3')
                        # else:
                        #     pygame.mixer.music.load('sounds/'+buttonResponse+'.mp3')
                        # pygame.mixer.music.set_volume(0.5)
                        # pygame.mixer.music.play()

                    if self.showNextButton == False:
                        if buttonResponse == "correct":
                            self.student.score += 1
                            self.student.rightAnswers.append([self.stageView.rightAnswer() +": " + self.stageModel.correctTag])
                            self.showNextButton = True

                        elif buttonResponse != None and buttonResponse != "null":
                            self.student.score -= 1
                            self.student.wrongAnswers.append(str(buttonResponse) +": " + self.stageModel.correctTag)

                    else:
                        buttonResponse = self.gameView.checkForNextButton(event)
                        if buttonResponse:
                            self.stageModel = stageModel.StageModel(self.domainModel)
                            self.stageView = stageView.StageView(self.stageModel, 150, 50, DISPLAYSURFACE)
                            self.student.currentStage += 1
                            self.writeFile()
                            self.showNextButton = False
                            self.stageView.clearDisplay()

                    """
                self.gameView.paintBackground()
                self.gameView.writeScore(self.user.score)
                self.gameView.writeStage(self.user.currentStage)
                self.stageView.paintBackground()
                self.stageView.writeQuestion()
                self.stageView.drawButtons()
                self.stageView.drawBorder()

                if self.showNextButton:
                    self.gameView.displayNextButton()

                pygame.display.update()
                self.fpsClock.tick(self.FPS)
                self.stageView.clearDisplay()

            else: #Start Menu Screen
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()

                    buttonResponse = self.startMenu.checkForStartButton(event)
                    if(buttonResponse == True) or (event.type == KEYDOWN and event.key == K_RETURN):
                        self.game = True

                self.startMenu.paintBackground()
                self.startMenu.writeStartMenu()
                self.startMenu.displayStartButton()

                pygame.display.update()
                self.fpsClock.tick(self.FPS)

    def checkCards(self,event):
        clickedCards = self.stageView.checkForCardClick(event)
        correctCount = 0
        if len(clickedCards) > 1:
            raise Exception()
        if len(clickedCards) == 1:
            card = clickedCards[0]
            if card.state is card.NONE:
                print("Testing %s against %s"%(self.stageModel.correctTag,card.individual.tags[self.stageModel.tagType]))
                if self.stageModel.correctTag in card.individual.tags[self.stageModel.tagType]:
                    card.setState(card.CORRECT)
                    correctCount += 1
                else:
                    card.setState(card.INCORRECT)
                    correctCount -= 1
        if correctCount >= 1:
            self.user.score+=1
            self.showNextButton=True

        elif correctCount == -1:
            self.user.score-=1

    def nextStage(self):
        self.stageModel = stageModel.StageModel(self.domainModel)
        self.stageView = stageView.StageView(self.stageModel, 100, 50, DISPLAYSURFACE)
        self.user.currentStage += 1
        self.showNextButton = False
        self.stageView.clearDisplay()

    def toJSON(self):
        base={}
        base["userModel"] = self.user.toJSON()
        base["stage"] = self.stageModel.toJSON()
        return base

    def fromJSON(self,json):
        self.user = userModel.User(json=json["userModel"])
        self.stageModel = stageModel.StageModel(self.domainModel,json=json["stage"])

