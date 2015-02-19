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
        #a list of 4 numbers, x, y, width, height
        self.rect = rect


class StageView:
    def __init__(self, stageModel, buttonStartX, buttonStartY, display):
        self.buttonStartX = buttonStartX
        self.buttonStartY = buttonStartY
        self.stageModel = stageModel
        self.answerButtons = self.initButtons()
        self.rectList = self.initRects()
        self.display = display
        

    def initButtons(self):
        x = self.buttonStartX
        y = self.buttonStartY
        numButtons = self.stageModel.numButtons
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
        x = self.buttonStartX
        y = self.buttonStartY
        numButtons = self.stageModel.numButtons

        for i in range(numButtons):
            rectList.append(HighlightRect( BLACK, 7, [x, y, 160, 160]))
            x += 200
            if x == 1250:
                x = 350
                y = 650
            print(rectList[i])

        return rectList

    def drawButtons(self):

        for i in range(len(self.rectList)):
                self.answerButtons[i].draw(self.display)
                pygame.draw.rect(self.display, self.rectList[i].color, self.rectList[i].rect, self.rectList[i].thickness)