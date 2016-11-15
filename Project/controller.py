import domainModel, random, pygame, sys, stageView, gameView, stageModel, userModel, startMenu, os.path, jsonIO
from pygame.locals import *

WINDOWWIDTH = 1500
WINDOWHEIGHT = 850
DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
USER_DATA_DIR = "userdata/"

class Controller:
    def __init__(self, domModel, userName):
        self.FPS = 30
        self.fpsClock = pygame.time.Clock()
        self.domainModel = domModel
        #self.userName = userName
        self.inMenu = False
        self.tagType="City"

        # No name represents debugging; no saves are made
        if userName != "" and os.path.isfile(USER_DATA_DIR+userName): #Check if there is already a file for this User
            try:
                self.fromJSON(jsonIO.loadFromJson(USER_DATA_DIR + userName))
            # TODO handle this better
            except BaseException as e:
                print("Unable to load save. Error:\n\t", e,"\n\t",type(e))
                self.user = userModel.User(userName)
                self.stageModel = stageModel.StageModel(domModel,self.tagType)
        else:
            self.user = userModel.User(userName)
            self.stageModel = stageModel.StageModel(domModel,self.tagType)

        self.startMenu = startMenu.StartMenu(DISPLAYSURFACE, self.user.username)
        self.stageView = stageView.StageView(self.stageModel, 100, 50, DISPLAYSURFACE)
        self.gameView = gameView.GameView(DISPLAYSURFACE)
        self.showNextButton = False

    def gameLoop(self):

        while True:
            if self.inMenu: #After clicking START (After Start Menu Screen)
                self.playLoop()
            else: #Start Menu Screen
                self.menuLoop()

    def playLoop(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                jsonIO.saveToJson(USER_DATA_DIR + self.user.username, self)
                pygame.quit()
                sys.exit()
            ###
            if self.showNextButton:
                buttonResponse = self.gameView.checkForNextButton(event)
                if buttonResponse or (event.type == KEYDOWN and event.key == K_RETURN):
                    self.nextStage()

            else:
                self.checkCards(event)
            ###
        self.gameView.render(self.user.score,self.user.currentStage)
        self.stageView.render()
        pygame.display.update()
        self.fpsClock.tick(self.FPS)
        self.stageView.clearDisplay()

    def menuLoop(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            buttonResponse = self.startMenu.checkForStartButton(event)
            if (buttonResponse == True) or (event.type == KEYDOWN and event.key == K_RETURN):
                self.inMenu = True

        self.startMenu.paintBackground()
        self.startMenu.writeStartMenu()
        self.startMenu.displayStartButton()

        pygame.display.update()
        self.fpsClock.tick(self.FPS)

    def checkCards(self,event):
        clickedCards = self.stageView.checkForCardClick(event)
        correctCount = 0
        if len(clickedCards) > 1:
            raise Exception()
        if len(clickedCards) == 1:
            card = clickedCards[0]
            if card.state is card.NONE:
                print("Testing %s against %s"%(self.stageModel.correctTag,card.individual.tags[self.stageModel.tagType]))
                if self.stageModel.correctTag in card.individual.tags[self.stageModel.tagType]:
                    card.setState(card.CORRECT)
                    correctCount += 1
                else:
                    card.setState(card.INCORRECT)
                    correctCount -= 1
        if correctCount >= 1:
            self.user.score+=1
            self.showNextButton=True

        elif correctCount == -1:
            self.user.score-=1

    def nextStage(self):
        self.stageModel = stageModel.StageModel(self.domainModel,self.tagType)
        self.stageView = stageView.StageView(self.stageModel, 100, 50, DISPLAYSURFACE)
        self.user.currentStage += 1
        self.showNextButton = False
        self.stageView.clearDisplay()

    def toJSON(self):
        base={}
        base["userModel"] = self.user.toJSON()
        base["stage"] = self.stageModel.toJSON()
        return base

    def fromJSON(self,json):
        self.user = userModel.User(json=json["userModel"])
        self.stageModel = stageModel.StageModel(self.domainModel,json=json["stage"])

