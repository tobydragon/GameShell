__author__ = "BenjaminWelsh"

import pygame, pygbutton, pygtools, color, TextWrap

class Card:
    def __init__(self, x, y, individual, title="", caption="", borderColor=color.BLACK, borderThickness=7):
        self.individual = individual
        self.borderColor = borderColor
        self.borderThickness = borderThickness
        self.title = title
        self.caption = caption
        self.state = self.NONE
        self.cardRect=pygame.Rect(x,y,200,250)
        self.x=x
        self.y=y
        self.fade=False
        self.symbol=self.NONE
        self.thumbnail=pygame.transform.scale(individual.image,(160,160))

        self.button=pygbutton.PygButton((x, y, 200, 250))

    def draw(self,display):
        display.blit(self.thumbnail,(self.x+20, self.y+20, 160, 160))
        font = pygame.font.SysFont("Courier", 19, True)
        symbolFont = pygame.font.SysFont("Segoe UI Symbol", 32)
        #titleDisplay = font.render(
        #    self.title.format(**self.individual.hrTags),
        #    True,
        #    color.BLACK)
        #display.blit(titleDisplay, (self.cardRect.x+20,self.cardRect.y+210))
        TextWrap.drawText(display,
                          self.title.format(**self.individual.hrTags),
                          color.BLACK,
                          pygame.Rect(self.cardRect.x+20,self.cardRect.y+185,160,65),
                          font,
                          True)

        pygtools.drawGoodRect(display, self.borderColor, self.cardRect, self.borderThickness)
        if self.fade:
            surf=pygame.Surface((self.cardRect.w-self.borderThickness,self.cardRect.h-self.borderThickness),pygame.SRCALPHA)
            surf.fill((255,255,255,200))
            display.blit(surf,(self.cardRect.x+self.borderThickness/2,self.cardRect.y+self.borderThickness/2))

        symbolDisplay = symbolFont.render(["", "","✔","✘"][self.symbol], True,
                                    (color.BLACK, color.BLUE, color.NICEGREEN, color.RED)[self.symbol])
        display.blit(symbolDisplay, (self.cardRect.x+self.cardRect.w-35, self.cardRect.y+self.cardRect.h-52))

    def setState(self,state):
        self.state=state
        self.borderColor=(color.BLACK, color.BLUE, color.NICEGREEN, color.RED)[state]

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