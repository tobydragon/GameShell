__author__ = 'JoãoGabriel'
import pygame, pygbutton

BLACK = (0, 0, 0)
LIGHTGREY = (160, 160, 160)

class GameView:
    def __init__(self, display):
        self.display = display
        self.nextButton = self.createNextButton('NEXT')

    def createNextButton(self, text):
        return pygbutton.PygButton((1200, 100, 120, 50), text)

    def paintBackground(self):
        pygame.draw.rect(self.display, LIGHTGREY, [0,0,1500,1000], 0)

    def writeScore(self, score):
        font = pygame.font.Font(None, 30)
        scoreRender = font.render("Score: "+str(score), True, BLACK)
        self.display.blit(scoreRender, [150, 20])

    def writeStage(self, stage):
        font = pygame.font.Font(None, 30)
        stageRender = font.render("Stage: "+str(stage), True, BLACK)
        self.display.blit(stageRender, [1250, 20])

    def displayNextButton(self):
        self.nextButton.draw(self.display)

    def checkForNextButton(self, event):
        buttonResponse = self.nextButton.handleEvent(event)
        if 'click' in buttonResponse:
            return True
