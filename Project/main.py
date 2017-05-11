__author__ = 'JoãoGabriel'
import pygame, controller, domainModel, settings, os, random, time
from pygame.locals import *

WINDOWWIDTH = 1500
WINDOWHEIGHT = 1000
WHITE = (255, 255, 255)

def main():

    pygame.init()
    pygame.display.set_caption('BioLab')

    #Create & load domain model
    domModel=domainModel.DomainModel(path=settings.DOMAIN_FILE)

    # generate install ID if none is found
    if not os.path.exists("userdata/InstallID1"):
        with open("userdata/InstallID1", "w") as idFile:
            random.seed(time.clock())
            id = ''.join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(9)])
            idFile.write(id)
    # load install ID
    with open("userdata/InstallID1") as idFile:
        userName = idFile.read()

    control = controller.Controller(domModel, userName)

    # Run main loop
    control.gameLoop()


main()
