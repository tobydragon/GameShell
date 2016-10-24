__author__ = 'JoãoGabriel'
import pygame, pygbutton, controller, os.path, enum, card, pygtools

class HighlightRect:
    def __init__(self, color, thickness, rect):
        self.color = color
        self.thickness = thickness
        #a list of 4 numbers, x, y, width, height
        self.rect = rect


class StageView:
    def __init__(self, stageModel, positionX, positionY, display):
        #self.buttonStartX = buttonStartX
        #self.buttonStartY = buttonStartY
        self.posX = positionX
        self.posY = positionY
        self.stageModel = stageModel
        self.answerButtons = self.initButtons()
        self.rectList = self.initRects()
        self.cardList=self.initCards()
        self.display = display
        self.display.fill(pygtools.WHITE)
        self.border = HighlightRect(pygtools.DARKGREEN, 7, [positionX, positionY, 1300, 750])

        #TEMP
        #self.card1=Card(positionX+50, positionY+150, stageModel.indList[0], "{category}")

    def initButtons(self):
        x = 150#self.buttonStartX
        y = 150#self.buttonStartY
        numButtons = self.stageModel.numButtons
        answerButtons = []

        for i in range(numButtons):
            indPath = self.stageModel.indList[i].imagepath
            indCate = self.stageModel.indList[i].tags["category"]
            indName = self.stageModel.indList[i].name
            if os.path.isfile(indPath):
                answerButtons.append(pygbutton.PygButton((x, y, 160, 160), normal=indPath, value=indCate))
            else:
                answerButtons.append(pygbutton.PygButton((x, y, 0, 0), normal= "images/MISSING_TEXTURE.png",value=indCate))
            x += 200
            if x == 1250:
                x = 350
                y = 550

        return answerButtons

    def initCards(self):
        cards = []
        numCards = len(self.stageModel.indList)
        x=50
        for i in range(min(numCards,5)):
            cards+=[card.Card(self.posX + x, self.posY + 150, self.stageModel.indList[i], "{category}")]
            x+=250
        return cards

    def initRects(self):
        rectList = []
        x = 150# self.buttonStartX
        y = 150#self.buttonStartY
        numButtons = self.stageModel.numButtons

        for i in range(numButtons):
            rectList.append(HighlightRect(pygtools.BLACK, 7, [x, y, 160, 160]))
            x += 200
            if x == 1250:
                x = 350
                y = 550

        return rectList

    def drawButtons(self):
        for i in range(len(self.rectList)):
                pass
                #self.answerButtons[i].draw(self.display)
                #pygame.draw.rect(self.display, self.rectList[i].color, self.rectList[i].rect, self.rectList[i].thickness)
        for card in self.cardList:
            card.draw(self.display)
        #self.card1.draw(self.display)

    def drawBorder(self):
        pygtools.drawGoodRect(self.display, self.border.color, self.border.rect, self.border.thickness)

    def paintBackground(self):
        pygame.draw.rect(self.display, pygtools.WHITE, [self.posX, self.posY, 1300, 750], 0)

    def writeQuestion(self):
        questionFont = pygame.font.Font(None, 70)
        question = questionFont.render(str(self.stageModel.category), True, pygtools.BLACK)
        self.display.blit(question, [self.posX + 50, self.posY + 50])

    def clearDisplay(self):
        self.display.fill(pygtools.WHITE)

    def checkForCardClick(self,event):
        """
        Handles a pygame event by passing it to each card.
        :param event: The pygame event to handle
        :return: a list of clicked cards
        """
        ret=[]
        for card in self.cardList:
            result = card.handleEvent(event)
            if result is "click":
                ret+=[card]
        return ret

    def checkForButtonClick(self, event, off):
        for buttonsLoop in range(len(self.answerButtons)):
                buttonResponse = self.answerButtons[buttonsLoop].handleEvent(event)
                if 'click' in buttonResponse:
                    if self.rectList[buttonsLoop].color != pygtools.BLACK or off:
                        return "null"
                    elif self.answerButtons[buttonsLoop].value == self.stageModel.category:
                        if off == False:
                            self.rectList[buttonsLoop].color = pygtools.GREEN
                        return "correct"
                    else:
                        if off == False:
                            self.rectList[buttonsLoop].color = pygtools.RED
                        return str(self.stageModel.indList[buttonsLoop].name)

    def rightAnswer(self):
        for i in range(len(self.answerButtons)):
            if self.stageModel.indList[i].category == self.stageModel.category:
                return self.stageModel.indList[i].name

