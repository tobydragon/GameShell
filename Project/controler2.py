import domainModel2, random, pygame, sys, stageView2, gameView, StageModel, stageView2
from pygame.locals import *

WINDOWWIDTH = 1500
WINDOWHEIGHT = 1000
DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

class Controller:
    def __init__(self, domModel, stageModel, stageView, gameView):
        self.FPS = 30
        self.fpsClock = pygame.time.Clock()
        self.domainModel = domModel
        self.stageModel = stageModel
        self.stageView = stageView
        self.gameView = gameView
        self.showNextButton = False
        self.score = 0

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
                        self.gameView.gameModel.score += 1
                        self.showNextButton = True

                    elif buttonResponse == "incorrect":
                        self.gameView.gameModel.score -= 1

                else:
                    buttonResponse = self.gameView.checkForNextButton(event)
                    if buttonResponse:
                        self.stageModel = StageModel.StageModel(self.domainModel)
                        self.stageView = stageView2.StageView(self.stageModel, 250, 450, DISPLAYSURFACE)
                        self.gameView.gameModel.stage += 1
                        self.showNextButton = False
                        self.stageView.clearDisplay()



            self.gameView.writeScore()
            self.gameView.writeStage()
            self.stageView.writeQuestion()
            self.stageView.drawButtons()

            if self.showNextButton:
                self.gameView.displayNextButton()

            pygame.display.update()
            self.fpsClock.tick(self.FPS)
            self.stageView.clearDisplay()





"""controller = Controller()
print(controller.domainModel)
stageModel = controller.createStageModel()
print(stageModel)"""



