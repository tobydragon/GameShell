import domainModel, random, pygame, sys, stageView, gameView, stageModel, userModel, startMenu, os.path
from pygame.locals import *

WINDOWWIDTH = 1500
WINDOWHEIGHT = 1000
DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
USER_DATA_DIR = "userdata/"

class Controller:
    def __init__(self, domModel, userName):
        self.FPS = 30
        self.fpsClock = pygame.time.Clock()
        self.domainModel = domModel
        self.userName = userName
        self.game = False

        if(os.path.isfile(USER_DATA_DIR+userName)): #Check if there is already a file for this User
            self.readFile()
        else:
            self.student = userModel.User(userName)
            self.stageModel = stageModel.StageModel(domModel)

        self.startMenu = startMenu.StartMenu(DISPLAYSURFACE, self.userName)
        self.stageView = stageView.StageView(self.stageModel, 250, 350, DISPLAYSURFACE)
        self.gameView = gameView.GameView(DISPLAYSURFACE)
        self.showNextButton = False


    def readFile(self):
        fileInput = open(USER_DATA_DIR+self.userName, "r")
        lines = fileInput.readlines()
        self.student = userModel.User(self.userName, lines[1:5]) #Passing lines (Score, Current Stage,  Right & Wrong Answers)
        self.stageModel = stageModel.StageModel(self.domainModel, lines[5], lines[6]) #Passing lines (Current Stage Category & Animals)


    def writeFile(self):
        file = open(USER_DATA_DIR+self.student.name, "w")
        file.truncate() #Clear file
        file.write(self.student.__repr__()) #Write Student Information
        file.write(self.stageModel.__repr__()) #Write Current Stage Information, for Loading PS: The last played answers will be in the end between []
        file.close()


    def gameLoop(self):

        while True:
            if self.game == True: #After clicking START (After Start Menu Screen)
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                        pygame.quit()
                        sys.exit()

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
                            self.student.rightAnswers.append([self.stageView.rightAnswer()+": "+self.stageModel.category])
                            self.showNextButton = True

                        elif buttonResponse != None and buttonResponse != "null":
                            self.student.score -= 1
                            self.student.wrongAnswers.append(str(buttonResponse)+": "+self.stageModel.category)

                    else:
                        buttonResponse = self.gameView.checkForNextButton(event)
                        if buttonResponse:
                            self.stageModel = stageModel.StageModel(self.domainModel)
                            self.stageView = stageView.StageView(self.stageModel, 250, 350, DISPLAYSURFACE)
                            self.student.currentStage += 1
                            self.writeFile()
                            self.showNextButton = False
                            self.stageView.clearDisplay()


                self.gameView.paintBackground()
                self.gameView.writeScore(self.student.score)
                self.gameView.writeStage(self.student.currentStage)
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
                    if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                        pygame.quit()
                        sys.exit()

                    buttonResponse = self.startMenu.checkForStartButton(event)
                    if(buttonResponse == True):
                        self.game = True

                self.startMenu.paintBackground()
                self.startMenu.writeStartMenu()
                self.startMenu.displayStartButton()

                pygame.display.update()
                self.fpsClock.tick(self.FPS)


