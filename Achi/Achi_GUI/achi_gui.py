import pygame
import sys 
import time 
from achi import Achi



SQUARE_SIZE = 150
BOARD_SIZE = 3

width = BOARD_SIZE * SQUARE_SIZE
height = BOARD_SIZE * SQUARE_SIZE
white = (255, 255, 255) 
line_color = (0, 0, 0)
brown = (160,82,45)
pygame.init() 
fps = 30
  
CLOCK = pygame.time.Clock() 

screen = pygame.display.set_mode((width, height)) 
pygame.display.set_caption("ACHI")

RED = pygame.transform.scale(
    pygame.image.load('red.png'),
    (SQUARE_SIZE//2, SQUARE_SIZE//2))
BLACK = pygame.transform.scale(
    pygame.image.load('black.png'),
    (SQUARE_SIZE//2, SQUARE_SIZE//2))

def game_initiating_window(): 
    screen.fill(brown) 
    
    pygame.draw.line(screen, line_color, (SQUARE_SIZE/2, SQUARE_SIZE/2), (width - SQUARE_SIZE/2, height - SQUARE_SIZE/2), 7) 
    pygame.draw.line(screen, line_color, (width-SQUARE_SIZE/2, SQUARE_SIZE/2), (SQUARE_SIZE/2, height - SQUARE_SIZE/2), 7) 
    pygame.draw.line(screen, line_color, (SQUARE_SIZE/2, SQUARE_SIZE/2), (SQUARE_SIZE/2, height - SQUARE_SIZE/2), 7)
    pygame.draw.line(screen, line_color, (width - SQUARE_SIZE/2, SQUARE_SIZE/2), (width-SQUARE_SIZE/2, height - SQUARE_SIZE/2), 7)
    pygame.draw.line(screen, line_color, (SQUARE_SIZE/2, SQUARE_SIZE/2), (width-SQUARE_SIZE/2, SQUARE_SIZE/2), 7)
    pygame.draw.line(screen, line_color, (SQUARE_SIZE/2, height - SQUARE_SIZE/2), (width-SQUARE_SIZE/2, height - SQUARE_SIZE/2), 7)
    pygame.draw.line(screen, line_color, (SQUARE_SIZE/2, 2*height/3 - SQUARE_SIZE/2), (width-SQUARE_SIZE/2, 2*height/3 - SQUARE_SIZE/2), 7)
    pygame.draw.line(screen, line_color, (2*width/3-SQUARE_SIZE/2, SQUARE_SIZE/2), (2*width/3 - SQUARE_SIZE/2, height - SQUARE_SIZE/2), 7) 

def isGameOver():
    return False

def draw_and_update(achi):
    game_initiating_window()
    place_pieces(achi)
    pygame.display.update()

def getPieceImage(piece):
    if piece == 1:
        return RED
    if piece == 2:
        return BLACK

def getPosFromSquare(i , j):
    return i*width//3 + SQUARE_SIZE//4, j*height//3 + SQUARE_SIZE//4

def place_pieces(achi):
    for i in range(3):
        for j in range(3):
            if achi.state[i][j] in [1,2]:
                piece = getPieceImage(achi.state[i][j])
                pos1, pos2 = getPosFromSquare(i, j)
                screen.blit(piece, (pos2,pos1))

def get_square_from_coordinates(i, j):
    return i*3+j

def getSquare(pos):
    x, y = pos
    x,y = y,x
    square_i, square_j = x // SQUARE_SIZE, y // SQUARE_SIZE
    return get_square_from_coordinates(square_i, square_j)
    

def game():
    achi = Achi()
    startSquare = None
    endSquare = None
    global turn
    turn = 2

    while not isGameOver():
        draw_and_update(achi)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif turn is 1:
                print("Thinking.....")
                achi.botMove()
                achi.count+=1
                turn = 2
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if turn is 2:
                    print("Your Turn")
                    startSquare = pygame.mouse.get_pos()
                    startSquare = getSquare(startSquare)
                
            elif event.type == pygame.MOUSEBUTTONUP:
                if turn is 2:
                    endSquare = pygame.mouse.get_pos()
                    endSquare = getSquare(endSquare)
                    key = achi.playerMove(startSquare,endSquare)
                    if key is 0:
                        turn = 1
                        achi.count+=1

    CLOCK.tick(60)

if __name__ == '__main__':
    game()

