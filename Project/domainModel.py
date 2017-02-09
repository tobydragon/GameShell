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
        if path:
            self.load(path)

    def __repr__(self):
        return (self.individualList.__repr__())

    def load(self, path):
        """
        Loads individuals from a domain file, appending them to the existing list.
        See wiki for file format
        :param path: path to file (csv format)
        """
        # Initializing the Individuals List
        indList = []
        header = None
        typeHeader = None
        with open(path, "r") as csvFile:
            reader = csv.reader(csvFile)
            for rowNum, row in enumerate(reader):
                if header is None:
                    header = row
                elif typeHeader is None and settings.DOMAIN_FIELD_TYPE_HEADER:
                    typeHeader = row
                else:
                    tags = {}
                    hrTags = {}  # Human readable
                    for k, v in zip(header, row):
                        if v:
                            tags[k] = v.split("|")
                            hrTags[k] = ", ".join(tags[k])  # generate human readable tag

                    # generate an id for the individual with the format <rowNumInFile>_<individual_name>
                    # Note: replaces spaces in the name with underscores
                    id = str(rowNum) + "_" + row[0].replace(" ", "_")
                    self.individualList.append(individual.Individual(row[0], id, row[1], tags, hrTags))
