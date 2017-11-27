#snake game

#import modules
import pygame
import sys
import random
import time
from pygame import locals

check_errors = pygame.init()

#check for errors
if check_errors[1] > 0:
    print("(!) Had {0} initializing errors, exiting".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialized!")
    
#play surface (set_mode expects a tuple)
playSurface = pygame.display.set_mode((720,460))
pygame.display.set_caption('Snake game!!!')

# Colors
red = pygame.Color(255,0,0)         #gameover
green = pygame.Color(0,255,0)       #snake 
black = pygame.Color(0,0,0)         #text
white = pygame.Color(255,255,255)   #screen
brown = pygame.Color(165,42,42)     #food

# FPS controller
fpsController = pygame.time.Clock()

# important variables
snakePos = [100, 50]                    # x, y
snakeBody = [[100,50],[90,50],[80,50]] 

foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]
foodSpawn = True

direction = 'RIGHT'
changeTo = direction

f = open('scores.txt', 'a+r')
if f.read() == '':
	f.write(str(0))
f.close()

f = open('scores.txt')
highScore = f.read()
highScore = int(highScore)
f.close()
score = 0

# gam over function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render('Game Over!', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (360, 15)
    playSurface.blit(GOsurf, GOrect)
       
    showScore(2)
    if score > highScore:
       
        f = open('scores.txt', 'w')
        f.write(str(score))
        f.close()
    pygame.display.flip()
    quitGame()
                
        

def showScore(choice = 1):
    sFont = pygame.font.SysFont('monaco', 24)
    sSurf = sFont.render('Score : {0}'.format(score), True, black)
    ssSurf = sFont.render('HighScore : {0}'.format(score), True, black)
    hsSurf = sFont.render('HighScore : {0}'.format(highScore), True, black)
    hsRect = hsSurf.get_rect()
    sRect = sSurf.get_rect()
    ssRect = ssSurf.get_rect()
    if choice == 1:
        #hsRect.midtop = (80, 10)
        sRect.midtop = (80, 10)
    else:
        if score < highScore:
            hsRect.midtop = (360, 120)
            sRect.midtop = (360, 160)
            playSurface.blit(hsSurf, hsRect)
            playSurface.blit(sSurf, sRect)
        else:
            ssRect.midtop = (360, 120)
            sRect.midtop = (360, 160)
            playSurface.blit(sSurf, sRect)
            playSurface.blit(ssSurf, ssRect)
    #playSurface.blit(hsSurf, hsRect)
    playSurface.blit(sSurf, sRect)
    #playSurface.blit(ssSurf, ssRect)

#game state
def quitGame():
    time.sleep(4)
    pygame.quit()       #quit pygame
    sys.exit()

# main logic of the game 
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == ord('d') or event.key == pygame.K_RIGHT:
                changeTo = 'RIGHT'
            if event.key == ord('a') or event.key == pygame.K_LEFT:
                changeTo = 'LEFT'
            if event.key == ord('w') or event.key == pygame.K_UP:
                changeTo = 'UP'
            if event.key == ord('s') or event.key == pygame.K_DOWN:
                changeTo = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                
    # validation of direction
    if changeTo == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if changeTo == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if changeTo == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if changeTo == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'
        
    if direction == 'RIGHT':
        snakePos[0] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'UP':
        snakePos[1] -= 10
    if direction ==  'DOWN':
        snakePos[1] += 10
        #[x,y]
        
    #snake body mecanism
    snakeBody.insert(0,list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()
        
    if foodSpawn == False:
        foodPos = [random.randrange(1,72)*10,random.randrange(1,46)*10]
    foodSpawn = True
    
    playSurface.fill(white)
    
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0],pos[1],10,10))
    
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0],foodPos[1],10,10))
    
    if snakePos[0] > 710 or snakePos[0] < 0:
        gameOver()
    if snakePos[1] > 450 or snakePos[1] < 0:
        gameOver()
    
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()
            
    showScore()
    pygame.display.flip()
    fpsController.tick(23)    
