import pygame as pg,sys
from pygame.locals import *
import time

#initialize global variables
init_XO    = 'x'
XO         = 'x'
N          = 4
winner     = None
draw       = False
width      = 400
height     = 400
white      = (255, 255, 255)
line_color = (10,10,10)

#TicTacToe NxN board
TTT = [[None for i in range(N)] for j in range(N)]

#initializing pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height+100),0,32)
pg.display.set_caption("Tic Tac Toe")

#loading the images
opening = pg.image.load('Opening.png')
x_img = pg.image.load('X.jpg')
o_img = pg.image.load('O.jpg')

#resizing images
x_img = pg.transform.scale(x_img, (80,80))
o_img = pg.transform.scale(o_img, (80,80))
opening = pg.transform.scale(opening, (width, height+100))


def game_opening():
    screen.blit(opening,(0,0))
    pg.display.update()
    time.sleep(1)
    screen.fill(white)
    
    # Drawing vertical lines
    pg.draw.line(screen,line_color,(width/N,0),(width/N, height),7)
    pg.draw.line(screen,line_color,(width/N*2,0),(width/N*2, height),7)
    # Drawing horizontal lines
    pg.draw.line(screen,line_color,(0,height/N),(width, height/N),7)
    pg.draw.line(screen,line_color,(0,height/N*2),(width, height/N*2),7)
    draw_status()
    

def draw_status():
    global draw

    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = 'Game Draw!'

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    # copy the rendered message onto the board
    screen.fill ((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width/2, 500-50))
    screen.blit(text, text_rect)
    pg.display.update()

def check_win():
    global TTT, winner,draw

	def line_check(line):
		if (line[0] == None):
			return False
		for i in range(N):
			if not(line[i] == line[0]):
				return False
		return True
	
    # check for winning rows
    for row in range (0,N):
        if line_check(TTT [row]):
            # this row won
            winner = TTT[row][0]
            pg.draw.line(screen, (250,0,0), (0, (row + 1)*height/N -height/6),\
                              (width, (row + 1)*height/N - height/(N*2) ), 4)
            break

    # check for winning columns
    for col in range (0, N):
		column = [TTT[i][col] for i in range(N)]
        if line_check(column):
            # this column won
            winner = TTT[0][col]
            #draw winning line
            pg.draw.line (screen, (250,0,0),((col + 1)* width/N - width/(N*2), 0),\
                          ((col + 1)* width/N - width/(N*2), height), 4)
            break

    # check for diagonal winners
	diag_1 = [TTT[i][i] for i in range(N)]
    if line_check(diag_1):
        # game won diagonally left to right
        winner = TTT[0][0]
        pg.draw.line (screen, (250,70,70), (50, 50), (350, 350), 4)
       
	diag_2 = [TTT[i][N-i-1] for i in range(N)]
    if line_check(diag_2):
        # game won diagonally right to left
        winner = TTT[0][N-1]
        pg.draw.line (screen, (250,70,70), (350, 50), (50, 350), 4)
    
    if(all([all(row) for row in TTT]) and winner is None):
        draw = True
    draw_status()


def drawXO(row,col):
    global TTT,XO
	posx = 30 + (row-1)*width/N
    posy = 30 + (col-1)*height/N
    
    TTT[row-1][col-1] = XO
    if(XO == 'x'):
        screen.blit(x_img,(posy,posx))
        XO ='o'
    else:
        screen.blit(o_img,(posy,posx))
        XO ='x'
    pg.display.update()

def userClick():
    #get coordinates of mouse click
    x,y = pg.mouse.get_pos()

    #get column of mouse click (1-3)
    if(x<width):
        col = int(x*N/width) + 1
    else:
        col = None
        
    #get row of mouse click (1-3)
	if(y<height):
        row = int(y*N/height) + 1
    else:
        row = None
    #print(row,col)
	
    if(row and col and TTT[row-1][col-1] is None):
        global XO
        #draw the x or o on screen
        drawXO(row,col)
        check_win()

def reset_game():
    global TTT, winner, XO, draw
    time.sleep(3)
    XO     = init_XO
    draw   = False
    game_opening()
    winner = None
    TTT    = [[None for i in range(N)] for j in range(N)]

game_opening()

# run the game loop forever
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type is MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            userClick()
            if(winner or draw):
                reset_game()
            
    pg.display.update()
    CLOCK.tick(fps)
