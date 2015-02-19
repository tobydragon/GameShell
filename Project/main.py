__author__ = 'JoãoGabriel'
import pygame, pygbutton, sys, stageView2, controler2, domainModel2, random
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 1500
WINDOWHEIGHT = 1000
WHITE = (255, 255, 255)

def createDomainModel(fileName):
        #Initializing the Individuals List
        indList = []

        fileInput = open(fileName, "r")
        lines = fileInput.readlines()
        lines = lines[1:]
        for line in lines:

            if(line[len(line)-1]) == '\n':
                line = line[0:len(line)-1]

            values = line.split(",")
            indList.append(domainModel2.Individual(values[0], values[1], values[2]))

        fileInput.close()

        random.shuffle(indList)

        #Initializing the Categories List and the Domain Model
        catList = ["Porifera", "Cnidaria", "Platyhelminthes", "Nematoda", "Mollusca", "Annelida", "Arthropoda", "Echinodermata", "Chordata"]
        random.shuffle(catList)

        #Create domModel
        domModel = domainModel2.DomainModel(catList, indList)
        return domModel

def main():
    #Creating Domain Model, Controller and first Stage Model
    domModel = createDomainModel("Animal Input.csv")
    controller = controler2.Controller(domModel)
    stageModel = controller.createStageModel()

    #NOT SURE IF THOSE SHOULD BE HERE OR IN THE CONTROLLER
    #Initializing Pygame
    windowBgColor = WHITE

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('BioLab')

    #Initial Score
    score = 0

    #Next Button
    nextButton = pygbutton.PygButton((1100, 850, 120, 50), 'NEXT')
    #INCOMPLETE

    myStageView = stageView2.StageView(stageModel, 250, 450, DISPLAYSURFACE)
    myStageView.drawButtons()

main()
