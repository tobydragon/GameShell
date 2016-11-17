__author__ = 'tdragon'

import random, domainModel, individual


class StageModel:
    def __init__(self, indList=None, tagType=None, correctTag=None, json=None):
        self.indList = indList
        self.correctTag = correctTag
        self.tagType = tagType
        if json:
            self.fromJSON(json)

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
