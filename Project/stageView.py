import pygame, pygbutton, sys, random, eztext, domainModel, controler


class HighlightRect:
    def __init__(self, color, thickness, rect):
        self.color = color
        self.thickness = thickness
        self.rect = rect


class StageView:
    def __init__(self, domModel, xRect, yRect, numButtons):
        self.xRect = xRect
        self.yRect = yRect
        self.numButtons = numButtons
        self.domModel = domModel
        self.answerButtons = self.initButtons()
        self.rectList = self.initRects()
        self.drawButtons(self.answerButtons, self.rectList)

    def initButtons(self):
        x = self.xRect
        y = self.yRect
        numButtons = self.numButtons
        indPath = domModel.individualList[0].imagepath
        indCate = domModel.individualList[0].category
        answerButtons = []
        for i in range(numButtons):
            indPath = domModel.individualList[i].imagepath
            indCate = domModel.individualList[i].category
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


    def drawButtons(rectList, answerButtons):

        for i in range(len(rectList)):
                answerButtons[i].draw(DISPLAYSURFACE)
                pygame.draw.rect(DISPLAYSURFACE, rectList[i].color, rectList[i].rect, rectList[i].thickness)
