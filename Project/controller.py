import domainModel, random, pygame, sys, stageView, gameView, stageModel, userModel, startMenu, os.path, jsonIO, stageController
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
        self.inMenu = False
        self.tagType = "City"
        self.tempScore = 0

        self.stageController = stageController.StageController(DISPLAYSURFACE)

        # No name represents debugging; no saves are made
        if userName != "" and os.path.isfile(USER_DATA_DIR+userName): #Check if there is already a file for this User
            try:
                self.fromJSON(jsonIO.loadFromJson(USER_DATA_DIR + userName))
            # TODO handle this better
            except BaseException as e:
                print("Unable to load save. Error:\n\t", e,"\n\t",type(e))
                self.user = userModel.User(userName)
                self.stageController.generateStageModel(domModel,self.tagType)
        else:
            self.user = userModel.User(userName)
            self.stageController.generateStageModel(domModel,self.tagType)

        self.startMenu = startMenu.StartMenu(DISPLAYSURFACE, self.user.username)
        self.gameView = gameView.GameView(DISPLAYSURFACE)
        #self.showNextButton = False

    def gameLoop(self):
        while True:
            if self.inMenu: #After clicking START (After Start Menu Screen)
                self.playLoop()
            else: #Start Menu Screen
                self.menuLoop()
            pygame.display.update()
            self.fpsClock.tick(self.FPS)

    def playLoop(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                jsonIO.saveToJson(USER_DATA_DIR + self.user.username, self)
                pygame.quit()
                sys.exit()
            ###
            if self.gameView.showNextButton:
                buttonResponse = self.gameView.checkForNextButton(event)
                if buttonResponse or (event.type == KEYDOWN and event.key == K_RETURN):
                    self.nextStage()

            else:
                score = self.stageController.checkCards(event)
                self.tempScore += score
                if score > 0:
                    self.gameView.showNextButton = True


        self.gameView.render(self.user.score,self.user.currentStage)
        self.stageController.renderStep(self.tempScore)
        self.gameView.renderButton()

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



    def nextStage(self):
        #self.stageModel = stageModel.StageModel(self.domainModel,self.tagType)
        #self.stageView = stageView.StageView(self.stageModel, 100, 50, DISPLAYSURFACE)
        self.user.currentStage += 1
        self.user.score += self.tempScore
        self.tempScore = 0
        self.gameView.showNextButton = False
        self.stageController.generateStageModel(self.domainModel,self.tagType)

        #self.stageView.clearDisplay()

    def toJSON(self):
        base={}
        base["userModel"] = self.user.toJSON()
        base["stageController"] = self.stageController.toJSON()
        return base

    def fromJSON(self,json):
        self.user = userModel.User(json=json["userModel"])
        self.stageController = stageController.StageController(DISPLAYSURFACE)
        self.stageController.fromJSON(json["stageController"])

