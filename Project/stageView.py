__author__ = 'JoãoGabriel'
import pygame, pygbutton, controller, os.path, enum
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DARKGREEN = (5, 102, 0)
LIGHTGREY = (212, 208, 200)
LIGHTBLUE = (153, 255, 255)

def drawGoodRect(display, color, rect,thickness):
    """
    Draws a pygame rectangle without little notches in the corners.
    :param display: The pygame display to draw to
    :param color: The color of the rectangle
    :param rect: The rectangle to draw
    :param thickness: The border's thickness
    :return:
    """
    rect = pygame.Rect(rect) #Convert list-style rect to pygame rect]
    halfThick=thickness/2.0
    pygame.draw.line(display, color, (rect.x,rect.y-halfThick+1), (rect.x,rect.y+rect.h+halfThick), thickness)
    pygame.draw.line(display, color, (rect.x,rect.y), (rect.x+rect.w+halfThick,rect.y), thickness)
    pygame.draw.line(display, color, (rect.x+rect.w+halfThick,rect.y+rect.h),  (rect.x,rect.y+rect.h), thickness)
    pygame.draw.line(display, color, (rect.x+rect.w,rect.y+rect.h),(rect.x+rect.w,rect.y), thickness)

class Card:
    def __init__(self, x, y, individual, title="", borderColor=BLACK, borderThickness=7):
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
        titleDisplay = font.render(self.title.format(**self.individual.tags), True, BLACK)
        display.blit(titleDisplay, (self.cardRect.x+20,self.cardRect.y+220))
        drawGoodRect(display, self.borderColor, self.cardRect, self.borderThickness)

    def setState(self,state):
        self.state=state
        self.borderColor=(BLACK,LIGHTBLUE,GREEN,RED)[state]

    def handleEvent(self,event):
        """
        Handles mouse events. Will pass the event to the internal button
        :param event:
        :return:
        """
        pass
    NONE=0
    SELECTED=1
    CORRECT=2
    INCORRECT=3

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
        self.positionX = positionX
        self.positionY = positionY
        self.stageModel = stageModel
        self.answerButtons = self.initButtons()
        self.rectList = self.initRects()
        self.cardList=self.initCards()
        self.display = display
        self.display.fill(WHITE)
        self.border = HighlightRect(DARKGREEN, 7, [positionX, positionY, 1200, 750])

        #TEMP
        self.card1=Card(positionX+50, positionY+150, stageModel.indList[0], "{category}")

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
        cards=[]

        return cards

    def initRects(self):
        rectList = []
        x = 150# self.buttonStartX
        y = 150#self.buttonStartY
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
                pass
                #self.answerButtons[i].draw(self.display)
                #pygame.draw.rect(self.display, self.rectList[i].color, self.rectList[i].rect, self.rectList[i].thickness)
        self.card1.draw(self.display)

    def drawBorder(self):
        drawGoodRect(self.display, self.border.color, self.border.rect, self.border.thickness)

    def paintBackground(self):
        pygame.draw.rect(self.display, WHITE, [self.positionX,self.positionY,1200,750], 0)

    def writeQuestion(self):
        questionFont = pygame.font.Font(None, 70)
        question = questionFont.render(str(self.stageModel.category), True, BLACK)
        self.display.blit(question, [self.positionX+50,self.positionY+50])

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
                        return str(self.stageModel.indList[buttonsLoop].name)

    def rightAnswer(self):
        for i in range(len(self.answerButtons)):
            if self.stageModel.indList[i].category == self.stageModel.category:
                return self.stageModel.indList[i].name

