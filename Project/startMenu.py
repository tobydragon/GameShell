__author__ = 'JoãoGabriel'
import pygame, pygbutton

BLACK = (0, 0, 0)
LIGHTGREY = (160, 160, 160)

class StartMenu:
    def __init__(self, display, student):
        self.display = display
        self.student = student
        self.startButton = self.createStartButton('START')

    def paintBackground(self):
        pygame.draw.rect(self.display, LIGHTGREY, [0,0,1500,1000], 0)

    def createStartButton(self, text):
        return pygbutton.PygButton((730, 700, 120, 50), text)

    def displayStartButton(self):
        self.startButton.draw(self.display)

    def writeStartMenu(self):
        font = pygame.font.Font(None, 38)
        stageRender = font.render("BioLab", True, BLACK) #Game Name
        self.display.blit(stageRender, [740, 500])
        font = pygame.font.Font(None, 30)
        stageRender = font.render("Welcome "+str(self.student), True, BLACK) #Student Welcome
        self.display.blit(stageRender, [720, 600])

    def checkForStartButton(self, event):
        buttonResponse = self.startButton.handleEvent(event)
        if 'click' in buttonResponse:
            return True