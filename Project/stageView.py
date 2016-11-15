__author__ = 'JoãoGabriel'
import pygame, pygbutton, controller, os.path, enum, card, color, pygtools

class HighlightRect:
    def __init__(self, color, thickness, rect):
        self.color = color
        self.thickness = thickness
        #a list of 4 numbers, x, y, width, height
        self.rect = rect


class StageView:
    def __init__(self, stageModel, positionX, positionY, display):
        self.posX = positionX
        self.posY = positionY
        self.stageModel = stageModel
        try:
            self.cardList=self.initCards()
        except Exception as e:
            print(e)
        self.display = display
        self.display.fill(color.WHITE)
        self.border = HighlightRect(color.DARKGREEN, 7, [positionX, positionY, 1300, 750])

    def initCards(self):
        cards = []
        numCards = len(self.stageModel.indList)
        if numCards>10:
            raise Exception("Too many cards (%i>10) to initialize all of them" % numCards)
        x=50
        for i in range(min(numCards,5)):
            cards.append(card.Card(self.posX + x, self.posY + 150, self.stageModel.indList[i], "Year:{Year Built}"))
            x+=250
        x=50
        if(numCards>5):
            for i in range(5,min(numCards, 10)):
                cards.append(card.Card(self.posX + x, self.posY + 450, self.stageModel.indList[i], "Year:{Year Built}"))
                x += 250
        return cards

    def drawButtons(self):
        for card in self.cardList:
            card.draw(self.display)
        #self.card1.draw(self.display)

    def drawBorder(self):
        pygtools.drawGoodRect(self.display, self.border.color, self.border.rect, self.border.thickness)

    def paintBackground(self):
        pygame.draw.rect(self.display, color.WHITE, [self.posX, self.posY, 1300, 750], 0)

    def writeQuestion(self):
        questionFont = pygame.font.Font(None, 70)
        question = questionFont.render(str(self.stageModel.correctTag), True, color.BLACK)
        self.display.blit(question, [self.posX + 50, self.posY + 50])

    def clearDisplay(self):
        self.display.fill(color.WHITE)

    def checkForCardClick(self,event):
        """
        Handles a pygame event by passing it to each card.
        :param event: The pygame event to handle
        :return: a list of clicked cards
        :rtype: Card
        """
        ret = []
        for card in self.cardList:
            response = card.handleEvent(event)
            if "click" in response:
                ret.append(card)
        return ret

    def render(self):
        self.paintBackground()
        self.writeQuestion()
        self.drawButtons()
        self.drawBorder()
