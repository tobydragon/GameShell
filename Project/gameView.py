__author__ = 'JoãoGabriel'
import pygame, pygbutton

BLACK = (0, 0, 0)
LIGHTGREY = (160, 160, 160)

class GameView:
    def __init__(self, display):
        self.display = display
        self.nextButton = self.createNextButton('NEXT')
        self.showNextButton=False

    def createNextButton(self, text):
        return pygbutton.PygButton((1200, 100, 120, 50), text)

    def paintBackground(self):
        pygame.draw.rect(self.display, LIGHTGREY, [0,0,1500,1000], 0)

    def writeScore(self, score,percent):
        font = pygame.font.SysFont("Courier", 22, True)
        scoreRender = font.render("Score: "+str(score)+"      Average percent correct: {:.2f}".format(float(percent)), True, BLACK)
        self.display.blit(scoreRender, [150, 20])

    def writeHelptext(self,):
        font = pygame.font.SysFont("Courier", 22, True)
        helpRender = font.render("Select The cards that match the question. Click the Check button when you're done. Then click the Next button to move to the next stage", True, BLACK)
        self.display.blit(helpRender, [30, 820])

    def writeStage(self, stage):
        font = pygame.font.SysFont("Courier", 22, True)
        stageRender = font.render("Stage: "+str(stage), True, BLACK)
        self.display.blit(stageRender, [1250, 20])

    def displayNextButton(self):
        self.nextButton.draw(self.display)

    def checkForNextButton(self, event):
        buttonResponse = self.nextButton.handleEvent(event)
        if 'click' in buttonResponse:
            return True

    def render(self,score,percent,stageNumber):
        self.paintBackground()
        self.writeScore(score,percent)
        self.writeStage(stageNumber)
        self.writeHelptext()

    def renderButton(self):
        if self.showNextButton:
            self.displayNextButton()