# Snake
# By Nicole Brown

import random, pygame, sys, time
from pygame.locals import *
from random import randint

BOARDSIZE=17 
FPS = 32 # frames per second, the general speed of the program
WINDOWWIDTH = 600 # size of window's width in pixels
WINDOWHEIGHT = 600 # size of windows' height in pixels
BOXSIZE = 30 # size of box height & width in pixels
GAPSIZE = 0 # size of gap between boxes in pixels
BOARDWIDTH = BOARDSIZE # number of columns of icons
BOARDHEIGHT = BOARDSIZE # number of rows of icons
cBOXSIZE = BOXSIZE
cXMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2 )
cYMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2 )

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
AQUA     = (0, 255, 255)
BLACK = (8 ,8 ,8)
BRIGHTGREEN = (127,255,0)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = RED

EMPTY = 'empty'
WALL = 'wall'
SNAKE = 'snake'
CIRCLE1 = 'circle1'
APPLE = 'apple'
ITEM = 'item'
pygame.init()

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

MOUSE_APPEAR_DELAY = 100

SnakeBody = [(4,4),(4,3),(4,2),(4,1)]
SnakeBody2 = [(8,4), (8,3), (8,2), (8,1)]
MinSnakeSize = 3
StartApplePos = (4, 7)
StartApplePos2 = (8, 7)
StartMousePos = (7, 10)
delayMouseAppear = MOUSE_APPEAR_DELAY
ChangeBody = 0
ChangeBody2 = 0
score = 0
score2 = 0
lastKey = 0
lastKey2 = 0
StartGameSpeed = 16
GameSpeed = StartGameSpeed
noPlayers = 0
increaseLength = ' '
increaseSpeed = ' '


while noPlayers < 1 or noPlayers > 2:
    print("Number of players (1-2): ")
    noPlayers = int(input())

while increaseSpeed != 'y' and increaseSpeed[:1] != 'n':
    print("Increase snake speed? (y/n)")
    increaseSpeed = input()

while increaseLength != 'y' and increaseLength != 'n':
    print("Increase snake length? (y/n)")
    increaseLength = input()
        

def main():
    global FPSCLOCK, DISPLAYSURF, pressButton, Level, score, score2, cBOXSIZE, cXMARGIN, cYMARGIN, lastKey, ChangeBody, lastKey2, ChangeBody2
    global delayMouseAppear, GameSpeed, noPlayers, increaseSpeed, increaseLength
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), RESIZABLE)
    Counter = 0


    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Snake')

    mainBoard = getBoard()
     
    pygame.display.update()

    DISPLAYSURF.fill(BGCOLOR)

    GameRunning = True
    GameRunning2 = True
    updateBoard = True
    while True: # main game loop
        FPSCLOCK.tick(FPS)

        Counter = Counter + 1    
       
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYUP and GameRunning and GameRunning2:
                updateBoard = True
                # check if the user pressed a key to move Snake
                if event.key == K_LEFT:
                    if lastKey != K_RIGHT:
                        lastKey = K_LEFT
                elif event.key == K_RIGHT:
                    if lastKey != K_LEFT:
                        lastKey = K_RIGHT
                elif event.key == K_UP:
                    if lastKey != K_DOWN:
                        lastKey = K_UP
                elif event.key == K_DOWN:
                    if lastKey != K_UP:
                        lastKey = K_DOWN

                # check if the user pressed a key to move Snake
                if noPlayers == 2:
                    if event.key == K_a:
                        if lastKey2 != K_d:
                            lastKey2 = K_a
                    elif event.key == K_d:
                        if lastKey2 != K_a:
                            lastKey2 = K_d
                    elif event.key == K_w:
                        if lastKey2 != K_s:
                            lastKey2 = K_w
                    elif event.key == K_s:
                        if lastKey2 != K_w:
                            lastKey2 = K_s


                        
            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                #Calculate new dimensions
                min_window = min(event.w, event.h)
                cWINDOWWIDTH = min_window
                cWINDOWHEIGHT = min_window
                cBOXSIZE = int(BOXSIZE*min_window/WINDOWWIDTH)
                cXMARGIN = int((cWINDOWWIDTH - (BOARDWIDTH * (cBOXSIZE + GAPSIZE))) / 2 )
                cYMARGIN = int((cWINDOWHEIGHT - (BOARDHEIGHT * (cBOXSIZE + GAPSIZE))) / 2 )
                drawBoard(mainBoard)
                pygame.display.update()
                
        if not GameRunning or not GameRunning2:
            continue

        if Counter % GameSpeed == 0:
            if lastKey != 0:
                GameRunning = moveSnake(mainBoard, lastKey)
                if increaseSpeed == 'y':
                    GameSpeed = int(StartGameSpeed - score/40)
                Counter = 0

            if lastKey2 != 0 and noPlayers == 2:
                GameRunning2 = moveSnake2(mainBoard, lastKey2)
                if increaseSpeed == 'y':
                    GameSpeed = int(StartGameSpeed - score2/40)
                Counter = 0

        SnakeX = SnakeBody[0][1]
        SnakeY = SnakeBody[0][0]

        #APPLE
        if mainBoard[SnakeX][SnakeY] == APPLE:
            mainBoard[SnakeX][SnakeY] = EMPTY
            score = score + 20
            delayMouseAppear = delayMouseAppear - 20
            if increaseLength == 'y':
                ChangeBody = ChangeBody + 1
            mainBoard[randint(2,BOARDSIZE-3)][randint(2,BOARDSIZE-3)] = APPLE
            
        #SPECIAL ITEM
        if mainBoard[SnakeX][SnakeY] == ITEM:
            mainBoard[SnakeX][SnakeY] = EMPTY
            if increaseLength == 'y':
                ChangeBody = ChangeBody - 1
            delayMouseAppear = MOUSE_APPEAR_DELAY
        if delayMouseAppear == 0:
            mainBoard[randint(2,BOARDSIZE-3)][randint(2,BOARDSIZE-3)] = ITEM
            delayMouseAppear = -1

        if noPlayers == 2:
            SnakeX = SnakeBody2[0][1]
            SnakeY = SnakeBody2[0][0]

            #APPLE
            if mainBoard[SnakeX][SnakeY] == APPLE:
                mainBoard[SnakeX][SnakeY] = EMPTY
                score2 = score2 + 20
                delayMouseAppear = delayMouseAppear - 20
                if increaseLength == 'y':
                    ChangeBody2 = ChangeBody2 + 1
                mainBoard[randint(2,BOARDSIZE-3)][randint(2,BOARDSIZE-3)] = APPLE
            
            #SPECIAL ITEM
            if mainBoard[SnakeX][SnakeY] == ITEM:
                mainBoard[SnakeX][SnakeY] = EMPTY
                if increaseLength == 'y':
                    ChangeBody2 = ChangeBody2 - 1
                delayMouseAppear = MOUSE_APPEAR_DELAY
            if delayMouseAppear == 0:
                mainBoard[randint(2,BOARDSIZE-3)][randint(2,BOARDSIZE-3)] = ITEM
                delayMouseAppear = -1
 
                
        DISPLAYSURF.fill(BGCOLOR) # drawing the window
       
        if Counter % GameSpeed == 0:
            message_display('Player 1 score:', int(2*cXMARGIN), int(cYMARGIN/2))
            message_display(str(score), int(3.5*cXMARGIN), int(cYMARGIN/2))
            if noPlayers == 2:
                message_display('Player 2 score:', int(cXMARGIN+0.7*cWINDOWWIDTH), int(cYMARGIN/2))
                message_display(str(score2), int(cXMARGIN+0.82*cWINDOWWIDTH), int(cYMARGIN/2))
            
            if not GameRunning or not GameRunning2:
                message_display('GAME OVER', 7*cXMARGIN, int(cYMARGIN/2))
            
            drawBoard(mainBoard)
            pygame.display.update()
            updateBoard = False
           
def moveSnake(board, lastKey):
    global ChangeBody
    #New position of snake head
    HitObstacle = False
    newSnakeX = SnakeBody[0][1]
    newSnakeY = SnakeBody[0][0]
    
    if lastKey == K_LEFT:
        newSnakeY = newSnakeY - 1
    elif lastKey == K_RIGHT:
        newSnakeY = newSnakeY + 1
    elif lastKey == K_UP:
        newSnakeX = newSnakeX - 1
    elif lastKey == K_DOWN:
        newSnakeX = newSnakeX + 1
            
    #Check here if the snake will hit the wall
    if board[newSnakeX][newSnakeY] == WALL:
        HitObstacle = True
    else:
        #Move snake
        if ChangeBody > 0:
            ChangeBody = ChangeBody - 1
        else:
            RemoveCount = 1 - ChangeBody
            if RemoveCount <= len(SnakeBody) - MinSnakeSize:
                for i in range(0, RemoveCount):
                    SnakeBody.pop() #Remove last part of tail
            ChangeBody = 0
        #Does the snake hit its body
        for pos in SnakeBody:
            if pos == (newSnakeY, newSnakeX):
                HitObstacle = True
                break            
        #Move head
        if not HitObstacle:
            SnakeBody.insert(0, (newSnakeY, newSnakeX))

    return not HitObstacle


def moveSnake2(board, lastKey):
    global ChangeBody2
    HitObstacle = False
    
    newSnakeX = SnakeBody2[0][1]
    newSnakeY = SnakeBody2[0][0]
    if lastKey == K_a:
        newSnakeY = newSnakeY - 1
    elif lastKey == K_d:
        newSnakeY = newSnakeY + 1
    elif lastKey == K_w:
        newSnakeX = newSnakeX - 1
    elif lastKey == K_s:
        newSnakeX = newSnakeX + 1
            
    #Check here if the snake will hit the wall
    if board[newSnakeX][newSnakeY] == WALL:
        HitObstacle = True
    else:
        #Move snake
        if ChangeBody2 > 0:
            ChangeBody2 = ChangeBody2 - 1
        else:
            RemoveCount = 1 - ChangeBody2
            if RemoveCount <= len(SnakeBody2) - MinSnakeSize:
                for i in range(0, RemoveCount):
                    SnakeBody2.pop() #Remove last part of tail
            ChangeBody2 = 0
        #Does the snake hit its body
        for pos in SnakeBody2:
            if pos == (newSnakeY, newSnakeX):
                HitObstacle = True
                break            
        #Move head
        if not HitObstacle:
            SnakeBody2.insert(0, (newSnakeY, newSnakeX))

    return not HitObstacle

       
def getBoard():
    global noPlayers
    board = []
    number = randint(1,7)
    number2 = randint(1,6)
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            if x==0 or x==BOARDWIDTH-1 or y==0 or y==BOARDHEIGHT-1:
                column.append(WALL)
            elif x == StartApplePos[1] and y == StartApplePos[0]:
                column.append(APPLE)
            elif noPlayers == 2 and x == StartApplePos2[1] and y == StartApplePos2[0]:
                column.append(APPLE)
            else:
                column.append(EMPTY)
                
        board.append(column)
    return board


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (cBOXSIZE + GAPSIZE) + cXMARGIN
    top = boxy * (cBOXSIZE + GAPSIZE) + cYMARGIN
    return (left, top)
       
        
def drawBoard(board):
    global noPlayers
    half =    int(cBOXSIZE * 0.5)
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if board[boxy][boxx] == EMPTY:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, cBOXSIZE, cBOXSIZE))
            elif board[boxy][boxx] == WALL:
                pygame.draw.rect(DISPLAYSURF, GRAY, (left, top, cBOXSIZE, cBOXSIZE))
            elif board[boxy][boxx] == APPLE:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, cBOXSIZE, cBOXSIZE))
                Image = pygame.image.load("strawberry.png")
                resizeImage = pygame.transform.scale(Image, (cBOXSIZE, cBOXSIZE))         
                DISPLAYSURF.blit(resizeImage,(left,top))
            elif board[boxy][boxx] == ITEM:
                pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, cBOXSIZE, cBOXSIZE))
                Image = pygame.image.load("mouse1.png")
                resizeImage = pygame.transform.scale(Image, (cBOXSIZE, cBOXSIZE))         
                DISPLAYSURF.blit(resizeImage,(left,top))
            #Check if snake body should be drawn
                
            for (x, y) in SnakeBody:
                #Head
                if x == SnakeBody[0][0] and y == SnakeBody[0][1]: 
                    if boxx == SnakeBody[0][0] and boxy == SnakeBody[0][1]:
                        pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, cBOXSIZE, cBOXSIZE))
                        if lastKey == K_LEFT:
                            Image = pygame.image.load("Snakeleft.jpg").convert_alpha()
                        elif lastKey == K_RIGHT:
                            Image = pygame.image.load("Snakeright.jpg").convert_alpha()    
                        elif lastKey == K_UP:
                            Image = pygame.image.load("Snakeup.jpg").convert_alpha()
                        elif lastKey == K_DOWN or lastKey == 0:
                            Image = pygame.image.load("Snake.jpg").convert_alpha()
                        resizeImage = pygame.transform.scale(Image, (cBOXSIZE, cBOXSIZE))         
                        DISPLAYSURF.blit(resizeImage,(left,top))
                #Body
                elif boxx == x and boxy == y:    
                    pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, cBOXSIZE, cBOXSIZE))
                    Image = pygame.image.load("body.png")
                    resizeImage = pygame.transform.scale(Image, (cBOXSIZE, cBOXSIZE))         
                    DISPLAYSURF.blit(resizeImage,(left,top))

            if noPlayers == 2:        
                for (x, y) in SnakeBody2:
                    #Head
                    if x == SnakeBody2[0][0] and y == SnakeBody2[0][1]: 
                        if boxx == SnakeBody2[0][0] and boxy == SnakeBody2[0][1]:
                            pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, cBOXSIZE, cBOXSIZE))
                            if lastKey2 == K_a:
                                Image = pygame.image.load("snake2left.jpg").convert_alpha()
                            elif lastKey2 == K_d:
                                Image = pygame.image.load("snake2right.jpg").convert_alpha()    
                            elif lastKey2 == K_w:
                                Image = pygame.image.load("snake2up.jpg").convert_alpha()
                            elif lastKey2 == K_s or lastKey2 == 0:
                                Image = pygame.image.load("snake2.jpg").convert_alpha()
                            resizeImage = pygame.transform.scale(Image, (cBOXSIZE, cBOXSIZE))         
                            DISPLAYSURF.blit(resizeImage,(left,top))
                    #Body
                    elif boxx == x and boxy == y:    
                        pygame.draw.rect(DISPLAYSURF, WHITE, (left, top, cBOXSIZE, cBOXSIZE))
                        Image = pygame.image.load("circle2.png")
                        resizeImage = pygame.transform.scale(Image, (cBOXSIZE, cBOXSIZE))         
                        DISPLAYSURF.blit(resizeImage,(left,top))
                                

                                
def message_display(text, left, top):
    largeText = pygame.font.Font('freesansbold.ttf', int(15*cBOXSIZE/BOXSIZE))
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (left,top)
    DISPLAYSURF.blit(TextSurf, TextRect)

def text_objects(text, font):
    textSurface = font.render(text, True, CYAN)
    return textSurface, textSurface.get_rect()
    
if __name__ == '__main__':
    main()


    
    
