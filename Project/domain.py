import pygame, pygbutton, sys, random, eztext
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



class HighlightRect:
    def __init__(self, color, thickness, rect):
        self.color = color
        self.thickness = thickness
        self.rect = rect

    
        

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

    #Student Name Inputs
    """txtbx = eztext.Input(maxlength=45, color=(255,0,0), prompt='type here: ')
    typed = events = pygame.event.get()"""


    #Initial Score, Image, Value & Correct
    score = 0
    correct = False
    current_value = 0

    #Rectangles Array
    rectArray = []

    #The Answers Buttons & White Right/Wrong Rectangles
    x = 250
    y = 450
    indPath = domModel.individualList[0].imagepath
    indCate = domModel.individualList[0].category
    numButtons = 9
    answerButtons = []
    for i in range(numButtons):
        indPath = domModel.individualList[i].imagepath
        indCate = domModel.individualList[i].category
        answerButtons.append(pygbutton.PygButton((x, y, 0, 0), normal=indPath, value=indCate))
        rectArray.append(HighlightRect( BLACK, 7, [x, y, 160, 160]))
        x += 200
        if x == 1250:
            x = 350
            y = 650
    

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
            for buttonsLoop in range(numButtons):
                
                if 'click' in answerButtons[buttonsLoop].handleEvent(event):
                    #If right, play sound, add score, change rect color to GREEN and open Next Button
                    if answerButtons[buttonsLoop].value == catList[current_value]:
                        pygame.mixer.music.load('sounds/Right.mp3')
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play()
                        score += 1
                        rectArray[buttonsLoop].color = GREEN
                        correct = True

                    #If wrong, play sound, sub score and change rect color to RED
                    else:
                        pygame.mixer.music.load('sounds/Wrong.mp3')
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play()
                        score -= 1
                        rectX = answerButtons[buttonsLoop].rect[0]
                        rectY = answerButtons[buttonsLoop].rect[1]
                        rectArray[buttonsLoop].color = RED
                       

            #Next Question Button Event
            if correct == True:
                if 'click' in nextButton.handleEvent(event):
                    current_value = (current_value+1)%numButtons
                    #random.shuffle(answerButtons)
                    for i in range(numButtons):
                        rectArray[i].color = BLACK

                    correct = False


            #Question
            questionFont = pygame.font.Font(None, 70)
            question = questionFont.render(str(catList[current_value]), True, BLACK)

            #Turn the BG in White
            DISPLAYSURFACE.fill(WHITE)
            #Display the Images on the screen
            for i in range(numButtons):
                answerButtons[i].draw(DISPLAYSURFACE)
                pygame.draw.rect(DISPLAYSURFACE, rectArray[i].color, rectArray[i].rect, rectArray[i].thickness)
                
            if correct == True:
                nextButton.draw(DISPLAYSURFACE)
            """txtbx.update(typed)"""
            

            ##Writing Score##
            font1 = pygame.font.Font(None, 30)
            text = font1.render("Score: "+str(score), True, BLACK)
            """txtbx.draw(DISPLAYSURFACE)"""
            DISPLAYSURFACE.blit(text, [150, 100])
            DISPLAYSURFACE.blit(question, [670, 300])

            pygame.display.update()
            FPSCLOCK.tick(FPS)

main()

