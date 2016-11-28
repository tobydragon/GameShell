import pygame, os, csv, individual

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
        header=None
        with open(path, "r") as csvFile:
            reader=csv.reader(csvFile)
            for i,row in enumerate(reader):
                if header is None:
                    header=row
                else:
                    tags = {}
                    hrTags={}
                    for k, v in zip(header, row):
                        if v:
                            tags[k] = v.split("|")
                            hrTags[k]=", ".join(tags[k])
                    id=str(i)+"_"+row[0].replace(" ","_")
                    self.individualList.append(individual.Individual(row[0],id, row[1], tags,hrTags))
        """lines = fileInput.readlines()
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
        """
        # Initializing the Categories List and the Domain Model
        # catList = ["Porifera", "Cnidaria", "Platyhelminthes", "Nematoda", "Mollusca", "Annelida", "Arthropoda", "Echinodermata", "Chordata"]
        # random.shuffle(catList)

        # Create domModel
