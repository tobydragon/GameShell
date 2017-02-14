import stageModel, domainModel, random, stageView, math, settings, individual, json

class StageController:
    def __init__(self, display, logger, knowledge, questionFile="questionTemplates.json"):
        ###Add knowledgeModel to parameter list to update after stage ends
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
        random.seed(3300)
        self.knowledge = knowledge

        if questionFile:
            print("loading question File")
            self.loadQuestionFile(questionFile)

    def generateStageModel(self,domainModel):
        print(self.questionTemplates)
        if self.questionTemplates:
            qtNum=math.floor(self.qStage/settings.STAGES_PER_QUESTION)%len(self.questionTemplates)
            print("using qTemp num",qtNum)
            qTemplate=self.questionTemplates[qtNum]
            self.tagType=qTemplate["TagType"]
            self.cardTitle=qTemplate["Title"]
            self.useCardImages=qTemplate["UseImage"]

        indList = domainModel.individualList[:]
        indList = [i for i in indList if individual.tagFilter(self.tagType)(i)]
        random.shuffle(indList)
        if (len(indList) > 10):
            indList=indList[:10]
        correctTag = random.choice(indList[random.randint(0, len(indList))-1].tags[self.tagType])
        self.stageModel = stageModel.StageModel(indList,self.tagType,correctTag)
        self._remakeStageView()

        self.stageFinished = False
        self.score = 0
        self.percent = 0
        self.qStage+=1

    def _remakeStageView(self):
        self.stageView = stageView.StageView(self.stageModel, 100, 50, self.display,self.cardTitle,self.useCardImages)
        self.stageView.nextButton.caption = "Check"

    def loopStepAll(self, event):
        """
        #Mode: All cards matching with check button
        Called for each action during the game loop.
        :param event: the pygame action
        :return: an integer score if stage complete. None otherwise
        """
        if self.stageFinished:
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
                #self.knowledge.updateScore(key, score)
                ##Must add parameter key and score before uncommenting updateScore call
                self.stageFinished=True


    def evaluateScore(self,score):
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
        clickedCards = self.stageView.checkForCardClick(event)
        if len(clickedCards) > 1:
            raise Exception()
        if len(clickedCards) == 1:
            card = clickedCards[0]

            if settings.LOG_SELECTIONS:
                self.logger.logAction("cardSelection",{"individualID":card.individual.id(),"selected":card.state is card.NONE})

            if card.state is card.NONE:
                card.setState(card.SELECTED)
            elif card.state is card.SELECTED:
                card.setState(card.NONE)

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

    def renderStep(self):
        self.stageView.render()

    def loadQuestionFile(self,fileName):
        try:
            f = open(fileName)
        except FileNotFoundError as e:
            print(e)
            raise e
        JSONdata = json.load(f)
        questionTemplates=JSONdata["questions"]
        random.shuffle(questionTemplates)
        self.questionTemplates=questionTemplates[:]
        #print(questionTemplates,self.questionTemplates)

    def toJSON(self):
        base = {}
        base["stage"] = self.stageModel.toJSON()
        return base


    def fromJSON(self, json):
        self.stageModel = stageModel.StageModel(json=json["stage"])
        self._remakeStageView()