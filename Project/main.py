__author__ = 'JoãoGabriel'
import pygame, pygbutton, sys, stageView, controller, domainModel, random, stageModel, gameView, os.path
from pygame.locals import *
#from libs.pygbutton import*

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
            indList.append(domainModel.Individual(values[0], values[1], values[2]))

        fileInput.close()

        random.shuffle(indList)

        #Initializing the Categories List and the Domain Model
        catList = ["Porifera", "Cnidaria", "Platyhelminthes", "Nematoda", "Mollusca", "Annelida", "Arthropoda", "Echinodermata", "Chordata"]
        random.shuffle(catList)

        #Create domModel
        domModel = domainModel.DomainModel(catList, indList)
        return domModel

def main():

    pygame.init()

    DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('BioLab')

    #Initialize Game
    domModel = createDomainModel("Animal Input.csv")
    stgModel = stageModel.StageModel(domModel)
    stgView = stageView.StageView(stgModel, 250, 350, DISPLAYSURFACE)
    gView = gameView.GameView(DISPLAYSURFACE)

    #Ask for the User Name
    print("Enter User Name:")
    userName = input()
    if(os.path.isfile(userName)):
        userData = []
        fileInput = open(userName, "r")
        lines = fileInput.readlines()
        lines = lines[1:] #We don't need the first line (userName)

        #Read lines and get data
        for line in lines:
            if(line[len(line)-1]) == '\n':
                line = line[0:len(line)-1]
                values = line.split(": ")
                userData.append(values[1])

            else:
                divide = line.split(":")
                values = str(divide[1]).split(",")
                for i in range(len(values)):
                    values[i] = values[i][1:]
                userData.append(values)
                print(values)


        stgModel = stageModel.StageModel(domModel, userData[2], userData[3])
        stgView = stageView.StageView(stgModel, 250, 350, DISPLAYSURFACE)
        control = controller.Controller(domModel, stgModel, stgView, gView, userName, userData)

    else:
        control = controller.Controller(domModel, stgModel, stgView, gView, userName)

    #The Game Loop
    control.gameLoop()

main()
