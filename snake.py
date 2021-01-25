import pygame
import random
import pickle

#https://stackoverflow.com/questions/23893978/keeping-high-scores-in-a-text-file für highscore
pygame.init()
pygame.display.set_caption("Snake")
biteSound = pygame.mixer.Sound('bite.wav')
failsound = pygame.mixer.Sound('fail.wav')
applePicture = pygame.image.load('applegood.png')


WIDTH = 600
HEIGHT = 300
BORDER = 15
SNAKEWIDTH = 15
SNAKESPEED = 15
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

screen = pygame.display.set_mode((WIDTH,HEIGHT+20))

class Apple:

    def __init__(self, length):
        self.length = length
        self.x = random.randrange(BORDER, WIDTH - BORDER - self.length,SNAKEWIDTH)
        self.y = random.randrange(BORDER, HEIGHT - BORDER - self.length,SNAKEWIDTH)
        self.score = 0
        
    
    def show(self):
        #alternative version with just a red square:
        #pygame.draw.rect(screen, RED, pygame.Rect( (self.x,self.y), (self.length,self.length)))
        screen.blit(applePicture, (self.x, self.y))


    def respawnApple(self):
        self.x = random.randrange(BORDER, WIDTH - BORDER - self.length,SNAKEWIDTH)
        self.y = random.randrange(BORDER, HEIGHT - BORDER - self.length,SNAKEWIDTH)



class Snake: 

    def __init__(self, x, y, squareLength):
        self.x = x
        self.y = y
        self.squareLength = squareLength
        self.bodyParts = [(self.x,self.y), (self.x-SNAKEWIDTH,self.y), (self.x-2*SNAKEWIDTH,self.y),(self.x-3*SNAKEWIDTH,self.y),(self.x-4*SNAKEWIDTH,self.y)]
        self.movingDirection = 1 # 0 = moving up; 1 = moving right; 2 = moving down; 3 = moving left
        self.savedMovingDirection = -1
        self.boolSavingMovingDirection = False
        self.score = 0
        self.failSoundPlayed = False

    def getHighscorePickle(self):
        highscoreLoad = pickle.load(open( "save.p", "rb" ) )

        for item in highscoreLoad:
            highscoreNew = item

        return int(highscoreNew)

    def setHighscorePickle(self):
        highscoreOld = self.getHighscorePickle()
        if highscoreOld < self.score:
            highscore = {self.score}
            pickle.dump( highscore, open( "save.p", "wb" ))

    def getHighscore(self):
        file1 = open("highscores.txt","r")

        highscore = file1.read()
        file1.close() 
        return int(highscore)

    def setHighscore(self):
        highscore = self.getHighscore()
        
        if highscore < self.score:
            file1 = open("highscores.txt","w+")
            file1.write(str(self.score))
            file1.close() 

    def updateBodyParts(self,appendBody):
        self.showSnake(BLACK)
        (x,y) = self.bodyParts[0]
        if self.movingDirection == 0:
            (x,y) = (x,y-SNAKESPEED) 
        elif self.movingDirection == 1:
            (x,y) = (x+SNAKESPEED,y)
        elif self.movingDirection == 2:
            (x,y) = (x,y+SNAKESPEED)
        elif self.movingDirection == 3:
            (x,y) = (x-SNAKESPEED,y)
        newBodyParts = [(x,y)]
        if len(self.bodyParts) > 1:
            if appendBody:
                for (a,b) in self.bodyParts:
                    newBodyParts.append((a,b))
            else:
                for (a,b) in self.bodyParts[0:-1]:
                    newBodyParts.append((a,b)) #Fehler: kopf der schlange bewegt sich mit 5 pixel/frame, der rest der schlange mit 15 pixel/frame, da man quasi zum vorgänger tupel wird. 
        else:
            if appendBody:
                newBodyParts.append(self.bodyParts[0])
        self.bodyParts = newBodyParts
        self.showSnake(WHITE)

    def changeMovingDirection(self):
        if self.savedMovingDirection == -1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.movingDirection != 2 :
                if self.bodyParts[0] [0] % SNAKEWIDTH == 0 and self.bodyParts[0] [1] % SNAKEWIDTH == 0:
                    self.movingDirection = 0
                else:
                    self.savedMovingDirection = 0
                    self.boolSavingMovingDirection = True
            if keys[pygame.K_RIGHT]and self.movingDirection != 3:
                if self.bodyParts[0] [0] % SNAKEWIDTH == 0 and self.bodyParts[0] [1] % SNAKEWIDTH == 0:
                    self.movingDirection = 1
                else:
                    self.savedMovingDirection = 1
                    self.boolSavingMovingDirection = True
            if keys[pygame.K_DOWN]and self.movingDirection != 0:
                if self.bodyParts[0] [0] % SNAKEWIDTH == 0 and self.bodyParts[0] [1] % SNAKEWIDTH == 0:
                    self.movingDirection = 2
                else:
                    self.savedMovingDirection = 2
                    self.boolSavingMovingDirection = True
            if keys[pygame.K_LEFT]and self.movingDirection != 1:
                if self.bodyParts[0] [0] % SNAKEWIDTH == 0 and self.bodyParts[0] [1] % SNAKEWIDTH == 0:
                    self.movingDirection = 3
                else:
                    self.savedMovingDirection = 3
                    self.boolSavingMovingDirection = True
        elif self.bodyParts[0] [0] % SNAKEWIDTH == 0 and self.bodyParts[0] [1] % SNAKEWIDTH == 0:
            self.movingDirection = self.savedMovingDirection
            self.savedMovingDirection = -1

    def showSnake(self,color):
        for (x,y) in self.bodyParts:
            pygame.draw.rect(screen, color, pygame.Rect( (x,y), (self.squareLength,self.squareLength)))

    def checkForCollision(self):
        #check for collision with wall
        if self.bodyParts [0] [0] < BORDER or self.bodyParts [0] [0]  > WIDTH - BORDER - self.squareLength or self.bodyParts [0] [1] < BORDER or self.bodyParts [0] [1] > HEIGHT - BORDER - self.movingDirection:
            return True
        #check for collision with itself
        for (x,y) in self.bodyParts[1:]:
            if self.bodyParts [0] == (x,y):
                return True
        return False

    def checkForAppleCollision(self,apple):
        if self.bodyParts[0] == (apple.x, apple.y):
            biteSound.play()
            self.score += 1
            apple.score += 1
            return True
        return False

    def stopSnake(self):
        pass

    def snakeRoutine(self, apple):
        self.changeMovingDirection()
        printOnScreen('Score: ' + str(self.score), BLACK, WIDTH//2-50, HEIGHT-10, 25)
        if not self.checkForCollision():
            if self.checkForAppleCollision(apple):
                snake.updateBodyParts(True)
                apple.respawnApple()
            else:
                snake.updateBodyParts(False)
            apple.show()
        else:
            self.setHighscorePickle()
            if not self.failSoundPlayed:
                failsound.play()
                self.failSoundPlayed = True
            #pygame.draw.rect(screen, BLACK, pygame.Rect( (WIDTH //2-85,HEIGHT//2-20), (190,70))) #black rectangle so that the white font can be read if the snake died in the middle
            #pygame.draw.line(screen, WHITE, (WIDTH //2-85,HEIGHT//2-20), (WIDTH //2-85+190,HEIGHT//2-20))
            #pygame.draw.line(screen, WHITE, (WIDTH //2-85,HEIGHT//2-20), (WIDTH //2-85,HEIGHT//2-20+70))
            #pygame.draw.line(screen, WHITE, (WIDTH //2-85,HEIGHT//2-20+70), (WIDTH //2-85+190,HEIGHT//2-20+70))
            #pygame.draw.line(screen, WHITE, (WIDTH //2-85+190,HEIGHT//2-20), (WIDTH //2-85+190,HEIGHT//2-20+70))
            apple.show()
            drawRectWithFrame(WIDTH //2-90,HEIGHT//2-30, 200,110, BLACK, WHITE)
            printOnScreen('Game Over!', WHITE, WIDTH //2-85, HEIGHT//2-20, 32)
            printOnScreen('Highscore: ' + str(self.getHighscorePickle()), WHITE, WIDTH //2-60, HEIGHT//2+20, 20)
            printOnScreen('Score: ' + str(self.score), WHITE, WIDTH //2-40, HEIGHT//2+50, 20)

        

def printOnScreen(text, color, width, height, fontSize):
    font = pygame.font.Font('freesansbold.ttf', fontSize)
    textInfo = font.render(text, False, color)
    screen.blit(textInfo, (width, height))

def drawRectWithFrame(x, y, width, height , colorRect, colorFrame):
    pygame.draw.rect(screen, colorRect, pygame.Rect( (x,y), (width, height)))
    pygame.draw.line(screen, colorFrame, (x,y), (x,y+height))
    pygame.draw.line(screen, colorFrame, (x,y), (x+width, y))
    pygame.draw.line(screen, colorFrame, (x, y+height), (x+width, y+height))
    pygame.draw.line(screen, colorFrame, (x+width, y), (x+width, y+height))


snake = Snake(150, HEIGHT//2, SNAKEWIDTH) # starting point has to be % 15 == 0 !!!!!! snake can't move otherwise
apple = Apple(SNAKEWIDTH)

run = True

#To reset the highscore, uncommand the following code :
"""pickleFirstEntry = {0}
pickle.dump( pickleFirstEntry , open( "save.p", "wb" ))"""

while run:
    #drawing a red line grid system for testing the movement of the snake
    """for w in range (WIDTH+10):
        if w % SNAKEWIDTH == 0:
            for h in range (HEIGHT+10):
                if h % SNAKEWIDTH == 0:
                    pygame.draw.line(screen, pygame.Color("red"), (0,h), (w, h))
                    pygame.draw.line(screen, pygame.Color("red"), (w,0), (w, h))"""

    #drawing the walls 
    pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect( (0,0), (WIDTH,BORDER))) #north wall
    pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect( (0,HEIGHT-BORDER), (WIDTH,BORDER+20))) #south wall 
    pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect( (0,0), (BORDER,HEIGHT))) #left wall 
    pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect( (WIDTH-BORDER,0), (BORDER,HEIGHT))) #right wall

    snake.snakeRoutine(apple)

    pygame.display.update()  


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.time.delay(100)
