__author__ = 'Kevin Pomer'


class UnitTestModel:
    def __init__(self):
        timeStamp_Window = 10

        tagCompetentThreshold = 0.8
        tagIncompetentThreshold = 0.2

        individualCompetentThreshold = 6
        individualIncompetentThreshold = -6

        def getTimeStampWindow():
            return timeStamp_Window

        def getTagCompetentThreshold():
            return tagCompetentThreshold

        def getTagIncompetentThreshold():
            return tagIncompetentThreshold

        def getIndividualCompetentThreshold():
            return individualCompetentThreshold

        def getIndividualIncompetentThreshold():
            return individualIncompetentThreshold

        #other fields?

    ##Getters (No Setters because Immutable)


class PlayTestModel:
    def __init__(self):
        timeStamp_Window = 3

        tagCompetentThreshold = 0.8
        tagIncompetentThreshold = 0.2

        individualCompetentThreshold = 2
        individualIncompetentThreshold = -2

        def getTimeStampWindow():
            return timeStamp_Window

        def getTagCompetentThreshold():
            return tagCompetentThreshold

        def getTagIncompetentThreshold():
            return tagIncompetentThreshold

        def getIndividualCompetentThreshold():
            return individualCompetentThreshold

        def getIndividualIncompetentThreshold():
            return individualIncompetentThreshold

        #Other fields?