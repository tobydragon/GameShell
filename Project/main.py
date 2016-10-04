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
        #catList = ["Porifera", "Cnidaria", "Platyhelminthes", "Nematoda", "Mollusca", "Annelida", "Arthropoda", "Echinodermata", "Chordata"]
        #random.shuffle(catList)

        #Create domModel
        domModel = domainModel.DomainModel(indList)
        return domModel

def main():

    pygame.init()
    pygame.display.set_caption('BioLab')

    #Create Domain Model
    domModel = createDomainModel("Buildings Domain 8.csv")

    #Ask for the User Name & Create Controller
    print("Enter User Name:")
    #userName = input() #Normal
    userName="" #DEBUG MODE
    control = controller.Controller(domModel, userName)

    #The Game Loop
    control.gameLoop()

main()
