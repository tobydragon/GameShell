import domainModel, random, pygame, sys, stageView, gameView, stageModel, userModel
from pygame.locals import *

WINDOWWIDTH = 1500
WINDOWHEIGHT = 1000
DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

class Controller:
    def __init__(self, domModel, stageModel, stageView, gameView, userName, userData = None):
        self.FPS = 30
        self.fpsClock = pygame.time.Clock()

        if(userData == None):
            self.student = userModel.User(userName)
        else:
            self.student = userModel.User(userName, userData)

        self.domainModel = domModel
        self.stageModel = stageModel
        self.stageView = stageView
        self.gameView = gameView
        self.showNextButton = False

    def writeFile(self):
        file = open(self.student.name, "w")
        file.truncate() #Clear file
        file.write("Name: "+self.student.name+"\n")
        file.write("Score: "+str(self.student.score)+"\n")
        file.write("Current Stage: "+str(self.student.currentStage)+"\n")
        file.write("Current Stage Category: "+str(self.stageModel.category)+"\n")
        file.write("Current Stage Animals: ")
        for i in range(len(self.stageModel.indList)):
            if(i == len(self.stageModel.indList)-1):
                file.write(str(self.stageModel.indList[i].name))
            else:
                file.write(str(self.stageModel.indList[i].name+", "))
        file.close()


    def gameLoop(self):

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                    pygame.quit()
                    sys.exit()


                    #Correct, Incorrect or "Already clicked"(null) decision
                buttonResponse = self.stageView.checkForButtonClick(event, self.showNextButton)
                if buttonResponse != None:
                    pygame.mixer.music.load('sounds/'+buttonResponse+'.mp3')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play()

                if self.showNextButton == False:
                    if buttonResponse == "correct":
                        self.student.score += 1
                        self.showNextButton = True

                    elif buttonResponse == "incorrect":
                        self.student.score -= 1

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




