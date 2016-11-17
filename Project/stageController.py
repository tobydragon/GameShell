import stageModel, domainModel, random, stageView

class StageController:
    def __init__(self, display):
        self.display = display

    def generateStageModel(self,domainModel,tagType):
        indList = domainModel.individualList[:]
        random.shuffle(indList)
        correctTag = random.choice(indList[random.randint(0, len(indList))-1].tags[tagType])
        self.stageModel = stageModel.StageModel(indList,tagType,correctTag)
        self.remakeStageView()

    def remakeStageView(self):
        self.stageView = stageView.StageView(self.stageModel, 100, 50, self.display)

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

    def renderStep(self,score):
        self.stageView.render(score)

    def toJSON(self):
        base = {}
        base["stage"] = self.stageModel.toJSON()
        return base


    def fromJSON(self, json):
        self.stageModel = stageModel.StageModel(json=json["stage"])
        self.remakeStageView()