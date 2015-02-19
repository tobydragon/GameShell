import domainModel2, random, pygame, sys

class Controller:
    def __init__(self, domModel):
        self.domainModel = domModel;
        #self.stageView = stageView [REMEMBER TO PUT IT BACK, AND THE PARAMETER TOO!]

    def createStageModel(self):
        catList = self.domainModel.categoryList
        random.shuffle(catList)
        category = catList[0]

        indList = self.domainModel.individualList
        random.shuffle(indList)

        animals = []
        for i in range(5):
            animals.append(indList[i])

        stageModel = StageModel(category, animals)
        return stageModel


    """def gameLoop(self, stageModel, gameView):"""


class StageModel:
    def __init__(self, category, individualList):
        self.category = category
        self.indList = individualList
        self.numButtons = len(individualList)

    def __repr__(self):
        print("Category: "+self.category)
        print("Individuals List: ")
        print(self.indList)


"""controller = Controller()
print(controller.domainModel)
stageModel = controller.createStageModel()
print(stageModel)"""



