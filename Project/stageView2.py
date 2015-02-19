__author__ = 'JoãoGabriel'
import pygame, pygbutton, controler2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
LIGHTGREY = (212, 208, 200)

class HighlightRect:
    def __init__(self, color, thickness, rect):
        self.color = color
        self.thickness = thickness
        self.rect = rect


class StageView:
    def __init__(self, stageModel, xRect, yRect, numButtons):
        self.xRect = xRect
        self.yRect = yRect
        self.numButtons = numButtons
        self.stageModel = stageModel
        self.answerButtons = self.initButtons()
        self.rectList = self.initRects()
        

    def initButtons(self):
        x = self.xRect
        y = self.yRect
        numButtons = self.numButtons
        answerButtons = []

        for i in range(numButtons):
            indPath = self.stageModel.indList[i].imagepath
            indCate = self.stageModel.indList[i].category
            answerButtons.append(pygbutton.PygButton((x, y, 0, 0), normal=indPath, value=indCate))
            x += 200
            if x == 1250:
                x = 350
                y = 650
            print(answerButtons[i])

        return answerButtons


    def initRects(self):
        rectList = []
        x = self.xRect
        y = self.yRect
        numButtons = self.numButtons

        for i in range(numButtons):
            rectList.append(HighlightRect( BLACK, 7, [x, y, 160, 160]))
            x += 200
            if x == 1250:
                x = 350
                y = 650
            print(rectList[i])

        return rectList

    def drawButtons(self, rectList, answerButtons, display):

        for i in range(len(self.rectList)):
                answerButtons[i].draw(display)
                pygame.draw.rect(display, rectList[i].color, rectList[i].rect, rectList[i].thickness)