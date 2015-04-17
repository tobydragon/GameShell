__author__ = 'tdragon'

import  random

class StageModel:
    def __init__(self, domainModel, category = None, indList = None):
        #First time playing
        if(category == None and indList == None):
            catList = domainModel.categoryList[:]
            random.shuffle(catList)
            self.category = catList[0]

            self.indList = domainModel.individualList
            self.numButtons = len(self.indList)
            random.shuffle(self.indList)
        #Recovering data from file
        else:
            self.category = category
            self.indList = indList
            for i in range(len(indList)):
                for j in range(len(domainModel.individualList)):
                    if(indList[i] == domainModel.individualList[j].name):
                        self.indList[i] = domainModel.individualList[j]
            self.numButtons = len(self.indList)


    def __repr__(self):
        print("Category: "+self.category)
        print("Individuals List: ")
        print(self.indList)

