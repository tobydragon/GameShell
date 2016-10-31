__author__ = 'tdragon'

import random


class StageModel:
    def __init__(self, domainModel, tagType="category", category=None, indList=None):
        self.domainModel = domainModel
        self.tagType=tagType
        # First time playing
        if (category == None and indList == None):
            self.indList = domainModel.individualList[:]
            random.shuffle(self.indList)
            self.correctTag = self.indList[random.randint(0, len(self.indList))-1].tags[tagType]
        # Recovering data from file
        else:
            self.retrieveData(category, indList)

    def retrieveData(self, category, indList):
        divide = category.split(": ")
        self.correctTag = divide[1][:len(divide[1]) - 1]  # Part after ": " and without the "\n" in the end

        divide = indList.split(":")
        indListLine = str(divide[1]).split(
            ",")  # Part after ":", doesn't catch the space after ":" because it will be needed
        for i in range(len(indListLine)):
            indListLine[i] = indListLine[i][1:]  # Take the Space from all the names

        indListLine[len(indListLine) - 1] = indListLine[len(indListLine) - 1][:len(indListLine[len(
            indListLine) - 1]) - 2]  # Takes off the "." on the last name in the Current Stage Animals list
        self.indList = indListLine

        for i in range(len(
                self.indList)):  # Turn the Names of the animals from IndList into Individuals Objects from Domain Model
            for j in range(len(self.domainModel.individualList)):
                if (self.indList[i] == self.domainModel.individualList[j].name):
                    self.indList[i] = self.domainModel.individualList[j]

    def __repr__(self):
        string = ("Current Stage Category: " + self.correctTag + "\n" +
                  "Current Stage Animals: ")
        for i in range(len(self.indList)):
            if (i == len(self.indList) - 1):
                string += (str(self.indList[i].name) + ".\n")
            else:
                string += (str(self.indList[i].name + ", "))

        return string

    def toJSON(self):
         # Not Implemented
        base={}
        base["correctTag"] = self.correctTag
        base["tagType"] = self.tagType
