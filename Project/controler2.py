import domainModel2, random, pygame, sys, stageView2
from pygame.locals import *


class Controller:
    def __init__(self, domModel, stageModel, stageView):
        self.FPS = 30
        self.fpsClock = pygame.time.Clock()
        self.domainModel = domModel
        self.stageModel = stageModel
        self.stageView = stageView

    def gameLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                #Correct or Incorrect decision
                buttonResponse = self.stageView.checkForButtonClick(event)

            self.stageView.drawButtons()
            pygame.display.update()
            self.fpsClock.tick(self.FPS)





"""controller = Controller()
print(controller.domainModel)
stageModel = controller.createStageModel()
print(stageModel)"""



