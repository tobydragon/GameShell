import domainModel2, random, pygame, sys, stageView2
from pygame.locals import *


class Controller:
    def __init__(self, domModel, stageModel, stageView):
        self.FPS = 30
        self.fpsClock = pygame.time.Clock()
        self.domainModel = domModel
        self.stageModel = stageModel
        self.stageView = stageView
        self.score = 0

    def gameLoop(self):

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                #Correct, Incorrect or "Already clicked"(null) decision
                buttonResponse = self.stageView.checkForButtonClick(event)
                if buttonResponse != None:
                    pygame.mixer.music.load('sounds/'+buttonResponse+'.mp3')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play()

                    if buttonResponse == "correct":
                        self.score += 1
                    elif buttonResponse == "incorrect":
                        self.score -= 1


            self.stageView.clearDisplay()
            self.stageView.writeScore(self.score)
            self.stageView.writeQuestion()
            self.stageView.drawButtons()
            pygame.display.update()
            self.fpsClock.tick(self.FPS)





"""controller = Controller()
print(controller.domainModel)
stageModel = controller.createStageModel()
print(stageModel)"""



