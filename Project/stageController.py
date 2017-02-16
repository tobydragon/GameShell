import stageModel, domainModel, random, stageView, math, settings, individual, json

class StageController:
    def __init__(self, display, logger, questionFile="insects_set.question_set.json"):
        """
        WARNING: generateStageModel MUST be called to use.
        :param display:
        """
        self.display = display
        self.stageFinished = False
        self.score = 0
        self.percent = 0
        self.logger = logger

        self.tagType = "Wing Type"
        self.cardTitle = "{Name}"
        self.useCardImages = True
        self.qStage=0
        self.questionTemplates=None
        self.stageModel=None
        if settings.RANDOM_SEED:
            random.seed(settings.RANDOM_SEED)

        if questionFile:
            print("loading question File")
            self.loadQuestionFile(questionFile)

    def _checkStageModelInit(self):
        if self.stageModel==None:
            raise Exception("Stagecontroller used without calling generateStageModel first.")

    def generateStageModel(self,domainModel):
        """
        Generates a new stage model, using the questionFile if specified.
        :param domainModel: The DomainModel to use
        :return: None
        """
        if self.questionTemplates:
            # get question number
            qtNum=math.floor(self.qStage/settings.STAGES_PER_QUESTION)%len(self.questionTemplates)
            print("using qTemplate num",qtNum)
            qTemplate=self.questionTemplates[qtNum]
            self.tagType=qTemplate["TagType"]
            self.cardTitle=qTemplate["Title"]
            self.useCardImages=qTemplate["UseImage"]

        indList = domainModel.individualList[:]
        # Filter indList to individuals that have the tagType of the question
        filterFunction = individual.createTagFilter(self.tagType)
        indList = [i for i in indList if filterFunction(i)]
        # Randomize the order
        random.shuffle(indList)
        if (len(indList) > 10):
            indList=indList[:10]

        # Choose the correct tag value by selecting an individual at random
        correctTag = random.choice(indList[random.randint(0, len(indList))-1].tags[self.tagType])
        self.stageModel = stageModel.StageModel(indList,self.tagType,correctTag)
        # Rebuild stageView with the new stageModel
        self._remakeStageView()

        self.stageFinished = False
        self.score = 0
        self.percent = 0
        self.qStage+=1

    def _remakeStageView(self):
        self._checkStageModelInit()
        self.stageView = stageView.StageView(self.stageModel, 100, 50, self.display,self.cardTitle,self.useCardImages)
        self.stageView.nextButton.caption = "Check"

    def loopStepAll(self, event):
        """
        #Mode: All cards matching with check button
        Called for each action during the game loop.
        :param event: the pygame action
        :return: (score, scorePercent) if stage complete. None otherwise
        """
        self._checkStageModelInit()

        if self.stageFinished:
            # Waiting for Next button to be clicked
            if self.stageView.checkNextButton(event):
                return self.score,self.percent
        else:
            self.updateCards(event)
            if self.stageView.checkNextButton(event):
                self.stageView.nextButton.caption="Next"
                cardResults = self.evaluateCardStates(True)
                self.score=self.evaluateScore(cardResults)
                self.percent=100.0*(cardResults["correct"]["selected"]+cardResults["incorrect"]["unselected"])/(len(self.stageView.cardList))
                self.stageView.scoreText="{}/{} correct. Score: {:.1F}/10.0".format(
                    cardResults["correct"]["selected"]+cardResults["incorrect"]["unselected"],len(self.stageView.cardList),self.score)
                self.stageFinished=True


    def evaluateScore(self,score):
        self._checkStageModelInit()

        coeff=4
        print(score)
        selectedCorrect = score["correct"]["selected"]
        unselectedIncorrect = score["incorrect"]["unselected"]
        correct=score["correct"]["total"]
        incorrect=score["incorrect"]["total"]
        total=score["total"]
        print("selectedCorrect %i  unselectedIncorrect %i  correct %i  incorrect %i  total %i"%(selectedCorrect,unselectedIncorrect,correct,incorrect,total))
        #calcScore=((selectedCorrect / correct) - (selectedCorrect / total)) + ((unselectedIncorrect / incorrect) - (unselectedIncorrect / total))
        if incorrect is 0:
            calcScore = selectedCorrect/correct
        else:
            calcScore=(selectedCorrect/correct)*(incorrect/total)+(unselectedIncorrect/incorrect)*(correct/total)
        print("score is:%.2f"%calcScore)
        return calcScore*10

    def evaluateCardStates(self, setCardFade = False):
        self._checkStageModelInit()

        results={"correct":{"selected":0,"unselected":0,"total":0},"incorrect":{"selected":0,"unselected":0,"total":0},"total":0}
        cardLogData = []
        for card in self.stageView.cardList:
            cardIsCorrect = self.stageModel.correctTag in card.individual.tags[self.stageModel.tagType]
            if cardIsCorrect is (card.state == card.SELECTED):
            #     correct += 1
                 card.symbol = card.CORRECT
            else:
            #     incorrect+=1
                 card.symbol = card.INCORRECT
            if not cardIsCorrect and setCardFade:
                 card.fade=True
            results["correct" if cardIsCorrect else "incorrect"]["selected" if card.state is card.SELECTED else "unselected"]+=1
            results["correct" if cardIsCorrect else "incorrect"]["total"]+=1
            results["total"]+=1
            if settings.LOG_STAGE_EVALS:
                cardLogData.append({
                    "individualID":card.individual.id(),
                    "selected":card.state is card.SELECTED,
                    "correctIndividual":cardIsCorrect
                })
        if settings.LOG_STAGE_EVALS:
            self.logger.logAction("stageEval",{
                "cards":cardLogData,
                "correctTag":self.stageModel.correctTag
            })
        print(results)
        return results

    def updateCards(self, event):
        """
        Passes event to cards, and updates any clicked card.
        If LOG_SELECTIONS is enabled in settings.py, logs any clicked cards as well
        :param event: pygame event
        :return: none
        """
        self._checkStageModelInit()

        clickedCards = self.stageView.checkForCardClick(event)
        if len(clickedCards) > 1:
            #Multiple cards being clicked with one mouse event makes no sense
            raise Exception()
        if len(clickedCards) == 1:
            card = clickedCards[0]

            if settings.LOG_SELECTIONS:
                self.logger.logAction("cardSelection",{"individualID":card.individual.id(),"selected":card.state is card.NONE})

            if card.state is card.NONE:
                card.setState(card.SELECTED)
            elif card.state is card.SELECTED:
                card.setState(card.NONE)

    def renderStep(self):
        self.stageView.render()

    def loadQuestionFile(self,fileName):
        try:
            with open(fileName) as f:
                JSONdata = json.load(f)
                questionTemplates = JSONdata["questions"]
                random.shuffle(questionTemplates)
                self.questionTemplates = questionTemplates[:]
        except FileNotFoundError as e:
            print(e)
            raise e
        
    def toJSON(self):
        base = {}
        base["stage"] = self.stageModel.toJSON()
        return base


    def fromJSON(self, json):
        self.stageModel = stageModel.StageModel(json=json["stage"])
        self._remakeStageView()

    """ # Unused old function
    def checkCards(self, event):
        clickedCards = self.stageView.checkForCardClick(event)
        correctCount = 0
        if len(clickedCards) > 1:
            raise Exception()
        if len(clickedCards) == 1:
            card = clickedCards[0]
            if card.state is card.NONE:
                print("Testing %s against %s" % (
                self.stageModel.correctTag, card.individual.tags[self.stageModel.tagType]))
                if self.stageModel.correctTag in card.individual.tags[self.stageModel.tagType]:
                    card.setState(card.CORRECT)
                    correctCount += 1
                else:
                    card.setState(card.INCORRECT)
                    correctCount -= 1
        if correctCount >= 1:
            return 1

        elif correctCount <= -1:
            return -1
        else:
            return 0
        """