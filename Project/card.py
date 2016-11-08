__author__ = "BenjaminWelsh"

import pygame, pygbutton, pygtools, color

class Card:
    def __init__(self, x, y, individual, title="", borderColor=color.BLACK, borderThickness=7):
        self.individual = individual
        self.borderColor = borderColor
        self.borderThickness = borderThickness
        self.title = title
        self.state = self.NONE
        self.cardRect=pygame.Rect(x,y,200,250)
        self.x=x
        self.y=y
        self.thumbnail=pygame.transform.scale(individual.image,(160,160))

        self.button=pygbutton.PygButton((x, y, 200, 250))

    def draw(self,display):
        display.blit(self.thumbnail,(self.x+20, self.y+20, 160, 160))
        font = pygame.font.Font(None, 32)
        titleDisplay = font.render(self.title.format(**self.individual.hrTags), True, color.BLACK)
        display.blit(titleDisplay, (self.cardRect.x+20,self.cardRect.y+220))
        pygtools.drawGoodRect(display, self.borderColor, self.cardRect, self.borderThickness)

    def setState(self,state):
        self.state=state
        self.borderColor=(color.BLACK, color.LIGHTBLUE, color.GREEN, color.RED)[state]

    def handleEvent(self,event):
        """
         Handles mouse events. Will pass the event to the internal button
        :param event:
        :return:
        """
        ret=self.button.handleEvent(event)
        return ret

    def __repr__(self):
        return self.individual

    NONE=0
    SELECTED=1
    CORRECT=2
    INCORRECT=3