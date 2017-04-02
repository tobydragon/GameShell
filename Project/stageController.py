import stageModel, domainModel, random, stageView, math, settings, individual, json

class StageController:
    def __init__(self, display, logger, knowledge, questionFile=None):
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

        self.tagType = "Name"
        self.cardTitle = "{Name}"
        self.useCardImages = True
        self.qStage=0
        self.questionTemplates=None
        self.stageModel=None
        if settings.RANDOM_SEED:
            random.seed(settings.RANDOM_SEED)
        self.knowledge = knowledge

        if questionFile:
            print("loading question File")
            self.loadQuestionFile(questionFile)
        elif settings.QUESTIONS_FILE:
            self.loadQuestionFile(settings.QUESTIONS_FILE)


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

        if len(indList)==0:
            print("ERROR: No individuals have the specified tagType %s"%self.tagType)
            raise Exception
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
                return self.score
        else:
            self.updateCards(event)
            if self.stageView.checkNextButton(event):
                self.stageView.nextButton.caption="Next"
                cardResults = self.evaluateCardStates(True)
                scoreInfo=ScoreInfo(cardResults)
                self.giveCardsValues(cardResults,scoreInfo)
                self.score=self.evaluateScore(cardResults,scoreInfo)

                #self.percent=100.0*(len(cardResults.correct)/(len(self.stageView.cardList)))
                self.stageView.scoreText="{}/{} correct. Points: {:.1F}".format(
                    len(cardResults.correct),len(self.stageView.cardList),self.score*100)


                self.knowledge.updateTagScore(self.tagType, self.score, cardResults)
                self.knowledge.checkCorrectCards(cardResults, scoreInfo)

                #Updates Score for tag based on what score the stage was given
                #SHould we call this updateCardScore() and within that checkCorrect/update?



                self.stageFinished=True

    def evaluateScore(self,cardStates,scoreInfo):
        self._checkStageModelInit()
        #calcScore=((selectedCorrect / correct) - (selectedCorrect / total)) + ((unselectedIncorrect / incorrect) - (unselectedIncorrect / total))
        calcScore=scoreInfo.rightVal*len(cardStates.correctRightTag)+scoreInfo.wrongVal*len(cardStates.correctWrongTag)
        print("score is:%.2f"%calcScore)
        return calcScore

    def giveCardsValues(self,cardStates,scoreInfo):
        for card in cardStates.rightTag:
            card.overlayCaption = str(round(100*scoreInfo.rightVal,1))
        for card in cardStates.wrongTag:
            card.overlayCaption = str(round(100*scoreInfo.wrongVal,1))

    def evaluateCardStates(self, setCardFade = False):
        self._checkStageModelInit()

        #results={"correct":{"selected":0,"unselected":0,"total":0},"incorrect":{"selected":0,"unselected":0,"total":0},"total":0}
        cardLogData = []
        selected=[]
        unselected=[]
        rightTag=[]
        wrongTag=[]
        for card in self.stageView.cardList:
            cardHasRightTag = self.stageModel.correctTag in card.individual.tags[self.stageModel.tagType]
            if cardHasRightTag:
                rightTag.append(card)
            else:
                wrongTag.append(card)

            if card.state==card.SELECTED:
                selected.append(card)
            else:
                unselected.append(card)
            """
            if cardHasRightTag is (card.state == card.SELECTED):
            #     correct += 1
                 card.symbol = card.CORRECT

            else:
            #     incorrect+=1
                 card.symbol = card.INCORRECT
                """

            if settings.LOG_STAGE_EVALS:
                cardLogData.append({
                    "individualID":card.individual.id(),
                    "selected":card.state is card.SELECTED,
                    "correctIndividual":cardHasRightTag
                })
        results=CardStateInfo(selected,unselected,rightTag,wrongTag)
        if setCardFade:
            for card in results.wrongTag:
                card.fade = True
        for card in results.correct:
            card.symbol=card.CORRECT

        for card in results.incorrect:
            card.symbol = card.INCORRECT

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
class ScoreInfo:
    def __init__(self,cardStates):
        if len(cardStates.rightTag)==0:
            self.rightVal=0
            self.wrongVal=1.0/len(cardStates.wrongTag)
        elif len(cardStates.wrongTag)==0:
            self.rightVal=1.0/len(cardStates.rightTag)
            self.wrongVal=0
        else:
            self.rightVal=0.5/len(cardStates.rightTag)
            self.wrongVal=0.5/len(cardStates.wrongTag)
        self.rightVal = math.ceil(self.rightVal*1000)/1000.0
        self.wrongVal = math.ceil(self.wrongVal * 1000) / 1000.0


class CardStateInfo:
    def __init__(self,selected,unselected,rightTag,wrongTag):
        self.selected=selected
        self.unselected=unselected
        self.rightTag=rightTag
        self.wrongTag=wrongTag
        self.correctRightTag = [i for i in selected if i in rightTag]
        self.correctWrongTag =[i for i in unselected if i in wrongTag]
        self.correct=self.correctRightTag+self.correctWrongTag
        self.incorrect=[i for i in unselected if i in rightTag]+[i for i in selected if i in wrongTag]
        assert(len(selected)+len(unselected)==len(rightTag)+len(wrongTag) and len(rightTag)+len(wrongTag)==len(self.correct)+len(self.incorrect))
        self.totalCount = len(self.correct) + len(self.incorrect)

    def __repr__(self):
        return "selected:%s\nunselected:%s\nrightTag%s\nwrongTag%s\ncorrect%s\nincorrect%s"%(str(self.selected),
                                                                                             str(self.unselected),
                                                                                             str(self.rightTag),
                                                                                             str(self.wrongTag),
                                                                                             str(self.correct),
                                                                                             str(self.incorrect))