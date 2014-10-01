import pygame, pygbutton, sys, random, csv
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 1500
WINDOWHEIGHT = 1000

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
LIGHTGRAY = (212, 208, 200)


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
        

def main():
    #Initializing the Individuals List
    indList = []
    
    fileInput = open("Animal Input.csv", "r")
    lines = fileInput.readlines()
    lines = lines[1:]
    for line in lines:
        
        if(line[len(line)-1]) == '\n':
            line = line[0:len(line)-1]
                
        values = line.split(",")
        indList.append(Individual(values[0], values[1], values[2]))
            
    random.shuffle(indList)
    
    #Initializing the Categories List and the Domain Model
    catList = ["Porifera", "Cnidaria", "Platyhelminthes", "Nematoda", "Mollusca", "Annelida", "Arthropoda", "Echinodermata", "Chordata"]
    random.shuffle(catList)
    domModel = DomainModel(catList, indList)
    print(domModel)

    #Initializing Pygame
    windowBgColor = WHITE

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('BioLab')


    #Initial Score, Image, Value & Correct
    score = 0
    correct = False
    current_value = 0

    #The Answers Buttons
    width = 350
    height = 450
    indPath = domModel.individualList[0].imagepath
    indCate = domModel.individualList[0].category
    answerButtons = []
    for i in range(9):
        indPath = domModel.individualList[i].imagepath
        indCate = domModel.individualList[i].category
        answerButtons.append(pygbutton.PygButton((width, height, 0, 0), normal=indPath, value=indCate))
        width += 170
        if width == 1200:
            width = 430
            height = 625

    #The Next Button
    nextButton = pygbutton.PygButton((1100, 850, 120, 50), 'NEXT')
    

    #Main Game Loop
    while True:
        #Event Handling Loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #Correct or Incorrect decision
            if 'click' in answerButtons[0].handleEvent(event):
                if answerButtons[0].value == catList[current_value]:
                    score += 1
                    correct = True
                    #asnwerButtons[0].normal = indList[0].pathright
                else:
                    score -= 1
                    #asnwerButtons[0].normal = indList[0].pathwrong

            if 'click' in answerButtons[1].handleEvent(event):
                if answerButtons[1].value == catList[current_value]:
                    score += 1
                    correct = True
                else:
                    score -= 1

            if 'click' in answerButtons[2].handleEvent(event):
                if answerButtons[2].value == catList[current_value]:
                    score += 1
                    correct = True
                else:
                    score -= 1

            if 'click' in answerButtons[3].handleEvent(event):
                if answerButtons[3].value == catList[current_value]:
                    score += 1
                    correct = True
                else:
                    score -= 1

            if 'click' in answerButtons[4].handleEvent(event):
                if answerButtons[4].value == catList[current_value]:
                    score += 1
                    correct = True
                else:
                    score -= 1

            if 'click' in answerButtons[5].handleEvent(event):
                if answerButtons[5].value == catList[current_value]:
                    score += 1
                    correct = True
                else:
                    score -= 1


            if 'click' in answerButtons[6].handleEvent(event):
                if answerButtons[6].value == catList[current_value]:
                    score += 1
                    correct = True
                else:
                    score -= 1

            if 'click' in answerButtons[7].handleEvent(event):
                if answerButtons[7].value == catList[current_value]:
                    score += 1
                    correct = True
                else:
                    score -= 1

            if 'click' in answerButtons[8].handleEvent(event):
                if answerButtons[8].value == catList[current_value]:
                    score += 1
                    correct = True
                else:
                    score -= 1


            #Next Question Button Event
            if correct == True:
                if 'click' in nextButton.handleEvent(event):
                    current_value = (current_value+1)%9
                    random.shuffle(answerButtons)
                    correct = False


            #Question
            questionFont = pygame.font.Font(None, 70)
            question = questionFont.render(str(catList[current_value]), True, BLACK)

            #Turn the BG in White
            DISPLAYSURFACE.fill(WHITE)
            #Display the Images on the screen
            for i in range(9):
                answerButtons[i].draw(DISPLAYSURFACE)
            if correct == True:
                nextButton.draw(DISPLAYSURFACE)
                

            ##Writing Score##
            font1 = pygame.font.Font(None, 30)
            text = font1.render("Score: "+str(score), True, BLACK)
            DISPLAYSURFACE.blit(text, [150, 100])
            DISPLAYSURFACE.blit(question, [670, 300])

            pygame.display.update()
            FPSCLOCK.tick(FPS)

main()
