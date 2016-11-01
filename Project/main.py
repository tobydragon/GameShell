__author__ = 'JoãoGabriel'
import pygame, pygbutton, sys, stageView, controller, domainModel, random, stageModel, gameView, os.path
from pygame.locals import *
#from libs.pygbutton import*

WINDOWWIDTH = 1500
WINDOWHEIGHT = 1000
WHITE = (255, 255, 255)

def main():

    pygame.init()
    pygame.display.set_caption('BioLab')

    #Create Domain Model
    domModel=domainModel.DomainModel(path="Buildings Domain 8.csv")

    #Ask for the User Name & Create Controller
    print("Enter User Name:")
    #userName = input() #Normal
    userName="dev" #DEBUG MODE
    control = controller.Controller(domModel, userName)

    #The Game Loop
    control.gameLoop()

main()
