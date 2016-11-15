__author__ = 'tdragon'

import random, domainModel, individual


class StageModel:
    def __init__(self, domainModel, tagType=None, json=None):
        self.domainModel = domainModel
        self.tagType=tagType
        if json:
            self.fromJSON(json)

        #TODO move this to a controller
        #Post Loading
        self.indList = domainModel.individualList[:]
        random.shuffle(self.indList)
        self.correctTag = random.choice(self.indList[random.randint(0, len(self.indList))-1].tags[self.tagType])



    def __repr__(self):
        string="stageModel: tagType=%s, correctTag=%s, len(indList)=%i" % (
            self.tagType,self.correctTag,len(self.indList)
        )
        return string

    def toJSON(self):
        base={}
        base["correctTag"] = self.correctTag
        base["tagType"] = self.tagType
        base["individuals"] = [i.toJSON() for i in self.indList]
        return base

    def fromJSON(self, json):
        self.correctTag = json["correctTag"]
        self.tagType = json["tagType"]
        self.indList = [individual.indFromJSON(i) for i in json["individuals"]]
