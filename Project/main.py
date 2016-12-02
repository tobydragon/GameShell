__author__ = 'JoãoGabriel'
import pygame, controller, domainModel, settings, os, random, time
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
    #userName="dev" #DEBUG MODE
    if not os.path.exists("userdata/InstallID1"):
        with open("userdata/InstallID1", "w") as idFile:
            random.seed(time.clock())
            #id=''.join([chr(random.randint(65,122)) for i in range(9)])
            id = ''.join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(9)])
            idFile.write(id)
    with open("userdata/InstallID1") as idFile:
        userName = idFile.read()
    #print(repr(userName))
    control = controller.Controller(domModel, userName)

    #The Game Loop
    control.gameLoop()

main()
