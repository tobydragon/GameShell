import stageModel, domainModel, random, stageView, math

class StageController:
    def __init__(self, display):
        """
        WARNING: generateStageModel MUST be called to use.
        :param display:
        """
        self.display = display
        self.stageFinished = False
        self.score = 0
        self.percent = 0

    def generateStageModel(self,domainModel,tagType):
        indList = domainModel.individualList[:]
        random.shuffle(indList)
        correctTag = random.choice(indList[random.randint(0, len(indList))-1].tags[tagType])
        self.stageModel = stageModel.StageModel(indList,tagType,correctTag)
        self._remakeStageView()

        self.stageFinished = False
        self.score = 0
        self.percent = 0

    def _remakeStageView(self):
        self.stageView = stageView.StageView(self.stageModel, 100, 50, self.display)
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
                self.score=self.evaluateScore(*cardResults)
                self.percent=100.0*cardResults[0]/(cardResults[0]+cardResults[1])
                print("Percent:",self.percent)
                self.stageView.scoreText="{}/{} correct. {:.1f}%. Score:{}".format(
                    cardResults[0],cardResults[0]+cardResults[1],self.percent,self.score)
                self.stageFinished=True


    def evaluateScore(self,correct,incorrect):
        coeff=4
        return math.floor(coeff*correct/(correct+incorrect))

    def evaluateCardStates(self, setCardFade = False):
        correct=0
        incorrect=0
        for card in self.stageView.cardList:
            cardIsCorrect=self.stageModel.correctTag in card.individual.tags[self.stageModel.tagType]
            if  cardIsCorrect is (card.state==card.SELECTED):
                correct+=1
                card.symbol=card.CORRECT
            else:
                incorrect+=1
                card.symbol = card.INCORRECT
            if not cardIsCorrect and setCardFade:
                card.fade=True
        return correct, incorrect

    def updateCards(self, event):
        clickedCards = self.stageView.checkForCardClick(event)
        if len(clickedCards) > 1:
            raise Exception()
        if len(clickedCards) == 1:
            card = clickedCards[0]
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

    def toJSON(self):
        base = {}
        base["stage"] = self.stageModel.toJSON()
        return base


    def fromJSON(self, json):
        self.stageModel = stageModel.StageModel(json=json["stage"])
        self._remakeStageView()