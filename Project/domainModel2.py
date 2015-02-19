class DomainModel:
    def __init__(self, categoryList, individualList):
        self.categoryList = categoryList
        self.individualList = individualList

    def __repr__(self):
        return(self.categoryList.__repr__()+self.individualList.__repr__())




class Individual:
    def __init__(self, name, category, imagepath):
        self.name = name
        self.category = category
        self.imagepath = imagepath


    def __repr__(self):
        return(self.name+" "+self.category+" "+self.imagepath)