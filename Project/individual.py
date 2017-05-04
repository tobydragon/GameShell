import pygame, os, settings, urlImage,time

__author__ = "BenjaminWelsh"


class Individual:
    def __init__(self, name, id, imagepath, tags, hrTags):
        if len(tags)==0:
            raise Individual.NoDataException("Individual with id {} created without any tags".format(id))
        self.name = name
        self.imagepaths = imagepath.split("|") if type(imagepath) is str else imagepath
        self._id = id
        self.images = {}

        for imagepath in self.imagepaths:
            if settings.IMAGEPATH_TEMPLATE!="" and settings.IMAGEPATH_TEMPLATE!=None:
                imagepath = settings.IMAGEPATH_TEMPLATE.format(imagepath)
            if os.path.exists(imagepath):
                self.addImage(pygame.image.load(imagepath))
            else:
                print("Unable to find image at '%s' for individual %s." % (imagepath, name))

        if not self.images:
            # Use MISSING_TEXTURE image if no images were loaded
            self.addImage(pygame.image.load("images/MISSING_TEXTURE.png"))
        if settings.DOMAIN_FILE=="wfb_dataset.csv":
            tempTime=time.clock()
            self.addImage(urlImage.fetchFlag(tags["cc"][0]),"flag")
            self.addImage(urlImage.fetchLocationImage(tags["Name"][0]),"map")
            print("TIME:",time.clock()-tempTime)

        # Dict Tagtype:[tags]
        self.tags = tags
        # human readable
        self.hrTags = hrTags

    def addImage(self, image, key="image"):
        if not key in self.images:
            self.images[key] =[]
        self.images[key].append(image)

    def id(self):
        return self._id

    def __repr__(self):
        return "<Individual> id=%s"%self._id#(self.name + " " + str(self.imagepaths) + "Tags: "+", ".join(self.tags))

    def toJSON(self):
        base = {}
        base["name"] = self.name
        base["id"] = self._id
        base["imagepaths"] = self.imagepaths
        base["tags"] = self.tags
        base["hrTags"] = self.hrTags
        return base

    class NoDataException(Exception):
        # Error for initializing without tags
        pass


def indFromJSON(json):
    return Individual(json["name"], json["id"], json["imagepaths"], json["tags"], json["hrTags"])

def individualFromCSVdata(row,rowNum,header,typeHeader=None):
    """
    Generates an individual from CSV data
    :param row: the current row as a list of strings
    :param rownum: the row number, used for creating the individualid
    :param header: the TagType header row
    :param typeHeader: the Tag
    :return:
    """
    tags={}
    hrTags={}
    for tagType, tagValue in zip(header, row):
        if tagValue:
            tags[tagType] = tagValue.split("|")  # split multiple tags on "|"
            hrTags[tagType] = ", ".join(tags[tagType])  # generate human readable tag

    # generate an id for the individual with the format <rowNumInFile>_<individual_name>
    # Note: replaces spaces in the name with underscores
    id = str(rowNum) + "_" + row[0].replace(" ", "_")
    return Individual(row[0], id, row[1], tags, hrTags)

def createTagFilter(*tags,imagetag=None):
    """
    Creates and returns a function that returns true if an individual has the tag tag.
    :param tag: The tag to filter for
    :return: a filter function
    """
    print("testing against:", tags)

    def filt(ind):
        #print("Testing",ind.id()," | ",ind.images," | ", tags," | ",imagetag)
        for tag in tags:
            if (not tag in ind.tags) or ind.tags[tag] == []:
                #print(ind.id(),"does not have tag",tag)
                return False
        if imagetag:
            if (not imagetag in ind.images) or ind.images[imagetag]==[None]:
                #print(ind.id(), "does not have image of type", imagetag)
                return False
        return True

    return filt
