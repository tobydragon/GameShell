__author__ = 'JoãoGabriel'
import pygame, controller, domainModel, settings
from pygame.locals import *
#from libs.pygbutton import*

WINDOWWIDTH = 1500
WINDOWHEIGHT = 1000
WHITE = (255, 255, 255)

def main():

    pygame.init()
    pygame.display.set_caption('BioLab')

    #Create Domain Model
    domModel=domainModel.DomainModel(path=settings.DOMAIN_FILE)

    #Ask for the User Name & Create Controller
    #userName = input() #Normal
    userName="dev" #DEBUG MODE
    control = controller.Controller(domModel, userName)

    #The Game Loop
    control.gameLoop()

main()
