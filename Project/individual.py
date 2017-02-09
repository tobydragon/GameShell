import pygame, os

__author__ = "BenjaminWelsh"


class Individual:
    def __init__(self, name, id, imagepath, tags, hrTags):
        self.name = name
        self.imagepaths = imagepath.split("|") if type(imagepath) is str else imagepath
        self._id = id
        self.images = []

        for imagepath in self.imagepaths:
            imagepath = "images_insects/" + imagepath + ".jpg"
            if os.path.exists(imagepath):
                self.images.append(pygame.image.load(imagepath))
            else:
                if not self.images:
                    self.images.append(pygame.image.load("images/MISSING_TEXTURE.png"))
                print("Unable to find image at '%s' for individual %s." % (imagepath, name))

        self.tags = tags
        # human readable
        self.hrTags = hrTags

    def id(self):
        return self._id

    def __repr__(self):
        return (self.name + " " + self.imagepaths + " " + str(self.tags))

    def toJSON(self):
        base = {}
        base["name"] = self.name
        base["id"] = self._id
        base["imagepaths"] = self.imagepaths
        base["tags"] = self.tags
        base["hrTags"] = self.hrTags
        return base


def indFromJSON(json):
    return Individual(json["name"], json["id"], json["imagepaths"], json["tags"], json["hrTags"])


def tagFilter(tag):
    def filt(ind):
        return tag in ind.tags and ind.tags[tag] != []

    return filt
