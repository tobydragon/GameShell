import pygame, os, settings

__author__ = "BenjaminWelsh"


class Individual:
    def __init__(self, name, id, imagepath, tags, hrTags):
        if len(tags)==0:
            raise Individual.NoDataException("Individual with id {} created without any tags".format(id))
        self.name = name
        self.imagepaths = imagepath.split("|") if type(imagepath) is str else imagepath
        self._id = id
        self.images = []

        for imagepath in self.imagepaths:
            if settings.IMAGEPATH_TEMPLATE!="" and settings.IMAGEPATH_TEMPLATE!=None:
                imagepath = settings.IMAGEPATH_TEMPLATE.format(imagepath)
            if os.path.exists(imagepath):
                self.images.append(pygame.image.load(imagepath))
            else:
                print("Unable to find image at '%s' for individual %s." % (imagepath, name))

        if not self.images:
            # Use MISSING_TEXTURE image if no images were loaded
            self.images.append(pygame.image.load("images/MISSING_TEXTURE.png"))

        self.tags = tags
        # human readable
        self.hrTags = hrTags

    def id(self):
        return self._id

    def __repr__(self):
        return (self.name + " " + str(self.imagepaths) + "Tags: "+", ".join(self.tags))

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


def createTagFilter(tag):
    """
    Creates and returns a function that returns true if an individual has the tag tag.
    :param tag: The tag to filter for
    :return: a filter function
    """
    def filt(ind):
        return tag in ind.tags and ind.tags[tag] != []

    return filt
