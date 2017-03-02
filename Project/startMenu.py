__author__ = 'JoãoGabriel'
import pygame, pygbutton, urlImage

BLACK = (0, 0, 0)
LIGHTGREY = (160, 160, 160)

class StartMenu:
    def __init__(self, display, student):
        self.display = display
        self.student = student
        self.startButton = self.createStartButton('START')

    def paintBackground(self):
        pygame.draw.rect(self.display, LIGHTGREY, [0,0,1500,1000], 0)
        logo = urlImage.fetchFlag("us")#urlImage.fetchLocationImage("United Arab Emirates")#pygame.image.load('images/biology_icon.jpg')
        self.display.blit(logo,(650,150))


    def createStartButton(self, text):
        return pygbutton.PygButton((690, 550, 120, 50), text)

    def displayStartButton(self):
        self.startButton.draw(self.display)

    def writeStartMenu(self):
        font = pygame.font.Font(None, 42)
        stageRender = font.render("BioLab", True, BLACK) #Game Name
        self.display.blit(stageRender, [700, 100])
        font = pygame.font.Font(None, 30)
        stageRender = font.render("Welcome!", True, BLACK) #Student Welcome
        self.display.blit(stageRender, [675, 450])
        font = pygame.font.Font(None, 18)
        stageRender = font.render("Developed by João Gama Vila Nova with the orientation of Dr. Toby Dragon", True, BLACK) #Student Welcome
        self.display.blit(stageRender, [550, 900])


    def checkForStartButton(self, event):
        buttonResponse = self.startButton.handleEvent(event)
        if 'click' in buttonResponse:
            return True