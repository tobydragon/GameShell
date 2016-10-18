class DomainModel:
    def __init__(self, individualList=[],path=""):
        self.individualList = individualList
        if path:
            self.load(path)

    def __repr__(self):
        return(self.individualList.__repr__())

    def load(self,path):
        # Initializing the Individuals List
        indList = []

        fileInput = open(path, "r")
        lines = fileInput.readlines()
        header = lines[0]
        keys = header.split(",")
        data = lines[1:]
        for line in data:

            if (line[-1]) == '\n': #Strip trailing newline
                line = line[0:-1]

            values = line.split(",")
            tags={}
            for k, v in zip(keys, values):
                if v:
                    tags[k]=v
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

        self.tags=tags

    def __repr__(self):
        return(self.name+" "+self.imagepath+" "+str(self.tags))