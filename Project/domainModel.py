import pygame, os

class DomainModel:
    def __init__(self, individualList=[],path=""):
        """
        Creates a new domain model.
        If run with no params, will create empty domain.
        If run with both params, will combine both sources
        :param individualList: a list of Individuals
        :param path: path to a domain file (.csv) to load from
        """
        self.individualList = individualList
        if path:
            self.load(path)

    def __repr__(self):
        return(self.individualList.__repr__())

    def load(self,path):
        """
        Loads individuals from a domain file, appending them to the existing list.
        See wiki for file format
        :param path: path to file (csv format)
        """
        # Initializing the Individuals List
        indList = []

        fileInput = open(path, "r")
        lines = fileInput.readlines()
        header = lines[0]
        if header[-1]=='\n':
            header=header[:-1]
        keys = header.split(",")
        data = lines[1:]
        for line in data:

            if (line[-1]) == '\n': #Strip trailing newline
                line = line[:-1]

            values = line.split(",")
            tags={}
            for k, v in zip(keys, values):
                if v:
                    tags[k] = v
            self.individualList.append(Individual(values[0], values[1], tags))

        fileInput.close()

        # Initializing the Categories List and the Domain Model
        # catList = ["Porifera", "Cnidaria", "Platyhelminthes", "Nematoda", "Mollusca", "Annelida", "Arthropoda", "Echinodermata", "Chordata"]
        # random.shuffle(catList)

        # Create domModel



class Individual:
    def __init__(self, name, imagepath, tags):
        self.name = name
        self.imagepath = imagepath

        if os.path.exists(imagepath):
            self.image=pygame.image.load(imagepath)
        else:
            self.image = pygame.image.load("images/MISSING_TEXTURE.png")
            print("Unable to find image at '%s' for individual %s."%(imagepath,name))

        print(type(self.image))
        self.tags = tags

    def __repr__(self):
        return(self.name+" "+self.imagepath+" "+str(self.tags))