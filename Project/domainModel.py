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
                    self.individualList.append(individual.individualFromCSVdata(row,rowNum,header,typeHeader))
