__author__ = "BenjaminWelsh"

import pygame, pygbutton, pygtools

class Card:
    def __init__(self, x, y, individual, title="", borderColor=pygtools.BLACK, borderThickness=7):
        self.individual = individual
        self.borderColor = borderColor
        self.borderThickness = borderThickness
        self.title = title
        self.state = self.NONE
        self.cardRect=pygame.Rect(x,y,200,250)


        self.button=pygbutton.PygButton((x+20, y+20, 160, 160), normal=individual.imagepath)

    def draw(self,display):
        self.button.draw(display)
        font = pygame.font.Font(None, 32)
        titleDisplay = font.render(self.title.format(**self.individual.tags), True, pygtools.BLACK)
        display.blit(titleDisplay, (self.cardRect.x+20,self.cardRect.y+220))
        pygtools.drawGoodRect(display, self.borderColor, self.cardRect, self.borderThickness)

    def setState(self,state):
        self.state=state
        self.borderColor=(pygtools.BLACK,pygtools.LIGHTBLUE,pygtools.GREEN,pygtools.RED)[state]

    def handleEvent(self,event):
        """
        Handles mouse events. Will pass the event to the internal button
        :param event:
        :return:
        """
        self.button.handleEvent(event)
        pass
    NONE=0
    SELECTED=1
    CORRECT=2
    INCORRECT=3