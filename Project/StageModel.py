__author__ = 'tdragon'

import domainModel2, random

class StageModel:
    def __init__(self, domainModel):
        catList = domainModel.categoryList.copy()
        random.shuffle(catList)
        self.category = catList[0]

        self.indList = domainModel.individualList
        self.numButtons = len(self.indList)
        random.shuffle(self.indList)

        animals = []
        for i in range(5):
            animals.append(self.indList[i])


    def __repr__(self):
        print("Category: "+self.category)
        print("Individuals List: ")
        print(self.indList)

