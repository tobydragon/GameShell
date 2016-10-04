class DomainModel:
    def __init__(self, individualList):
        self.individualList = individualList

    def __repr__(self):
        return(self.individualList.__repr__())




class Individual:
    def __init__(self, name, category, imagepath):
        self.name = name
        self.category = category
        self.imagepath = imagepath

        self.tags={}
        self.tags["category"]=category

    def __repr__(self):
        return(self.name+" "+self.imagepath+" "+str(self.tags))