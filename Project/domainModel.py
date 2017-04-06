import pygame, os, csv, individual, settings


class DomainModel:
    def __init__(self, individualList=[], path=""):
        """
        Creates a new domain model.
        If run with no params, will create empty domain.
        If run with both params, will combine both sources
        :param individualList: a list of Individuals
        :param path: path to a domain file (.csv) to load from
        """
        self.individualList = individualList
        self.questionTagTypeDict = {"Development": ["Anamorphic", "Ametabolous", "Hemimatabolous", "Holometabolous"],
                                    "MouthParts": ["Entognathous", "Chewing", "Piercing-Sucking"],
                                    "WingType": ["Wingless", "Membranous", "Straight", "Fringed",
                                                 "Covered With Scales"]}
        # {questionTagType:[questionTags]} - Links tags with tagTypes rather than just with individuals
        # Do we need one for {questionTag: [Individuals]} or is that covered when we get the individialList

        if path:
            self.load(path)

    def __repr__(self):
        return self.individualList.__repr__()

    def load(self, path):
        """
        Loads individuals from a domain file, appending them to the existing list.
        See wiki for file format
        :param path: path to file (csv format)
        """
        header = None
        typeHeader = None
        with open(path, "r") as csvFile:
            reader = csv.reader(csvFile)
            for rowNum, row in enumerate(reader):
                if header is None:
                    # Save the first row as the header
                    header = row
                elif typeHeader is None and settings.DOMAIN_FIELD_TYPE_HEADER:
                    # Save the second row as the typeHeader if enabled in settings.py
                    typeHeader = row
                else:
                    # Process each line of data
                    if len(row)<2:
                        # ignore blank lines
                        continue
                    tags = {}
                    hrTags = {}  # Human readable
                    for tagType, tagValue in zip(header, row):
                        if tagValue:
                            tags[tagType] = tagValue.split("|") # split multiple tags on "|"
                            hrTags[tagType] = ", ".join(tags[tagType])  # generate human readable tag

                    # generate an id for the individual with the format <rowNumInFile>_<individual_name>
                    # Note: replaces spaces in the name with underscores
                    id = str(rowNum) + "_" + row[0].replace(" ", "_")
                    self.individualList.append(individual.Individual(row[0], id, row[1], tags, hrTags))
