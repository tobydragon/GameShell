import domainModel, random, pygame, sys, stageView, gameView, stageModel, knowledgeModel, knowledgeSettings
import userModel, startMenu, os.path, jsonIO, stageController, settings
from pygame.locals import *
import logger

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
        self.tempScore = 0

        self.logger = logger.Logger(userName, settings.DOMAIN_FILE)
        ##Create KnowledgeModel Settings objects to pass to self.knowledge
        playtestSettings = knowledgeSettings.PlayTestModel()
        unittestSettings = knowledgeSettings.UnitTestModel()
        ##

        ##Select either test above to send to knowledgeModel
        self.knowledge = knowledgeModel.KnowledgeModel(domModel.questionTagTypeDict, self.domainModel.individualList, playtestSettings)
        self.stageController = stageController.StageController(DISPLAYSURFACE,self.logger, self.knowledge)

        # No name represents debugging; no saves are made
        if userName != "" and os.path.isfile(
                                USER_DATA_DIR + userName + ".json"):  # Check if there is already a file for this User
            try:
                # Load the file using self.fromJSON
                self.fromJSON(jsonIO.loadFromJson(USER_DATA_DIR + userName + ".json"))
            # TODO handle this better
            except BaseException as e:
                # If the load is unsuccessful, print a warning, and generate a new user.
                print("Unable to load save. Error:\n\t", e, "\n\t", type(e))
                self.user = userModel.User(userName)
                self.stageController.generateStageModel(domModel)
        else:
            # No file found, or no username(i.e. dev mode)
            if (userName != ""):
                print("No save for user {} found".format(userName))
            self.user = userModel.User(userName)
            self.stageController.generateStageModel(domModel)

        self.startMenu = startMenu.StartMenu(DISPLAYSURFACE, self.user.username)
        self.gameView = gameView.GameView(DISPLAYSURFACE)


    def gameLoop(self):
        """
        Main game loop.
        Calls playLoop or menuLoop depending on current state
        :return: None
        """
        while True:
            if self.inMenu:  # After clicking START (After Start Menu Screen)
                self.playLoop()
            else:  # On Start Menu Screen
                self.menuLoop()
            pygame.display.update()
            self.fpsClock.tick(self.FPS)

    def playLoop(self):
        """
        Main loop function for playing the game
        :return: None
        """

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                # Exit code
                self.gameView.paintBackground()
                font = pygame.font.Font(None, 64)
                stageRender = font.render("Saving Logs for exit", True, (0, 0, 0))
                DISPLAYSURFACE.blit(stageRender, [50, 50])

                pygame.display.update()
                if self.user.username != "dev":
                    # save gamestate
                    jsonIO.saveToJson(USER_DATA_DIR + self.user.username + ".json", self)
                    # save event log & email data
                    if self.logger.containsData and self.user.username != "dev_save":
                        self.logger.saveForExit()
                        self.logger.sendEmail(self.user.username)
                pygame.quit()
                sys.exit()
            ###
            # Update stage and get result
            stageResult = self.stageController.loopStepAll(event)
            # If the stage has been completed
            if stageResult:
                self.user.score += stageResult
                self.user.addScore(stageResult)
                self.nextStage()

        # Render screen
        self.gameView.render(self.user.score*100, self.user.getAverageScore()*100, self.user.currentStage)
        self.stageController.renderStep()
        self.gameView.renderButton()

    def menuLoop(self):
        """
        Loop code during menu
        :return: None
        """
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
        """
        Moves to the next stage, calling stageController.generateStageModel to create it
        :return: None
        """
        self.user.currentStage += 1
        self.user.score += self.tempScore
        self.tempScore = 0
        self.gameView.showNextButton = False
        self.stageController.generateStageModel(self.domainModel)

    def toJSON(self):
        base = {}
        base["userModel"] = self.user.toJSON()
        base["stageController"] = self.stageController.toJSON()
        return base

    def fromJSON(self, json):
        self.user = userModel.User(json=json["userModel"])
        self.stageController.fromJSON(json["stageController"])
        ##Model user fromJSON for knowledgeModel