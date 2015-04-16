__author__ = 'JoãoGabriel'
import pygame, pygbutton, controller

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARKGREEN = (5, 102, 0)
LIGHTGREY = (212, 208, 200)
LIGHTBLUE = (153, 255, 255)

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
        self.display.fill(WHITE)
        self.border = HighlightRect(DARKGREEN, 7, [150, 150, 1200, 600])
        

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
                y = 550

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
                y = 550

        return rectList

    def drawButtons(self):
        for i in range(len(self.rectList)):
                self.answerButtons[i].draw(self.display)
                pygame.draw.rect(self.display, self.rectList[i].color, self.rectList[i].rect, self.rectList[i].thickness)

    def drawBorder(self):
        pygame.draw.rect(self.display, self.border.color, self.border.rect, self.border.thickness)

    def paintBackground(self):
        pygame.draw.rect(self.display, WHITE, [150,150,1200,600], 0)

    def writeQuestion(self):
        questionFont = pygame.font.Font(None, 70)
        question = questionFont.render(str(self.stageModel.category), True, BLACK)
        self.display.blit(question, [600, 200])

    def clearDisplay(self):
        self.display.fill(WHITE)

    def checkForButtonClick(self, event, off):
        for buttonsLoop in range(len(self.answerButtons)):
                buttonResponse = self.answerButtons[buttonsLoop].handleEvent(event)
                if 'click' in buttonResponse:
                    if self.rectList[buttonsLoop].color != BLACK or off:
                        return "null"
                    elif self.answerButtons[buttonsLoop].value == self.stageModel.category:
                        if off == False:
                            self.rectList[buttonsLoop].color = GREEN
                        return "correct"
                    else:
                        if off == False:
                            self.rectList[buttonsLoop].color = RED
                        return "incorrect"

