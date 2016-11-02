import pygame, os

__author__="BenjaminWelsh"

class Individual:
    def __init__(self, name, imagepath, tags, hrTags):
        self.name = name
        self.imagepath = imagepath

        if os.path.exists(imagepath):
            self.image=pygame.image.load(imagepath)
        else:
            self.image = pygame.image.load("images/MISSING_TEXTURE.png")
            print("Unable to find image at '%s' for individual %s."%(imagepath,name))

        self.tags = tags
        # human readable
        self.hrTags = hrTags

    def __repr__(self):
        return(self.name+" "+self.imagepath+" "+str(self.tags))

    def toJSON(self):
        base = {}
        base["name"] = self.name
        base["imagepath"] = self.imagepath
        base["tags"] = self.tags
        base["hrTags"] = self.hrTags
        return base

def indFromJSON(json):
    return Individual(json["name"],json["imagepath"],json["tags"],json["hrTags"])