import domainModel2, random, pygame, sys, stageView2

class Controller:
    def __init__(self, domModel, stageModel, stageView):
        self.FPS = 30
        self.fpsClock = pygame.time.Clock()
        self.domainModel = domModel
        self.stageModel = stageModel
        self.stageView = stageView

    def gameLoop(self):
        while True:
            self.stageView.drawButtons()
            pygame.display.update()
            self.fpsClock.tick(self.FPS)





"""controller = Controller()
print(controller.domainModel)
stageModel = controller.createStageModel()
print(stageModel)"""



