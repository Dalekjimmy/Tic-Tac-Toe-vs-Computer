import pygame
import numpy as np
import sys
import time
import random
pygame.init()
pygame.font.init()
Board = np.array([[0,0,0],[0,0,0],[0,0,0]])
screen = pygame.display.set_mode((600, 600+40))
screen.fill((255,255,255))
pygame.display.set_caption('Tic-Tac-Toe')
pygame.draw.rect(screen,(0,0,0),(0,600,600,40))
default_font = pygame.font.get_default_font()
font_renderer = pygame.font.Font(default_font, 30)
Winner = 0
Player = random.randrange(-1,2,2)
def draw_board():
    pygame.draw.line(screen,(0,0,0),(0,200),(600,200),5)
    pygame.draw.line(screen,(0,0,0),(0,400),(600,400),5)
    pygame.draw.line(screen,(0,0,0),(200,0),(200,600),5)
    pygame.draw.line(screen,(0,0,0),(400,0),(400,600),5)
    pygame.draw.line(screen,(0,0,0),(0,600),(600,600),5)
def Draw_Shapes(Center,Player):
    if Player==1:
        pygame.draw.line(screen, (0, 0, 0), (Center[0]-80, Center[1]-80), (Center[0]+80, Center[1]+80), 5)
        pygame.draw.line(screen, (0, 0, 0), (Center[0]-80, Center[1]+80), (Center[0]+80, Center[1]-80), 5)
    elif Player==-1:
        pygame.draw.circle(screen, (0, 0, 0), [Center[0], Center[1]], 80,5)
def Position(Board,Player,Winner):
    if Winner == 0 and Player == 1:
        A = np.array(pygame.mouse.get_pos())
        C1, C2 = A[0]+100-A[0]%200, A[1] +100 -A[1]%200
        Center = [C1,C2]
        if Board[int((C2-100)/200),int((C1-100)/200)]==0:
            Draw_Shapes(Center,Player)
            Board[int((C2-100)/200),int((C1-100)/200)] = Player
            return Player * (-1)
        else:
            return Player
def Win(Board):
    for a in range(3):
        if sum(Board[:,a])==3 or sum(Board[a,:])==3 or\
                Board[0,0]+Board[1,1]+Board[2,2] == 3 or Board[0,2]+Board[1,1]+Board[2,0] == 3:
            return 1
        elif sum(Board[:,a])==-3 or sum(Board[a,:])==-3 or\
                Board[0,0]+Board[1,1]+Board[2,2] == -3 or Board[0,2]+Board[1,1]+Board[2,0] == -3:
            return -1
    return 0
def Final_Winner(Board):
    for a in range(3):
        if sum(Board[:, a]) == 3 or sum(Board[a, :]) == 3 or \
                Board[0, 0] + Board[1, 1] + Board[2, 2] == 3 or Board[0, 2] + Board[1, 1] + Board[2, 0] == 3:
            label = font_renderer.render("Player 1 Wins!", 1, (255, 255, 255))
            screen.blit(label, (200, 600))
            return -1
        elif sum(Board[:, a]) == -3 or sum(Board[a, :]) == -3 or \
                Board[0, 0] + Board[1, 1] + Board[2, 2] == -3 or Board[0, 2] + Board[1, 1] + Board[2, 0] == -3:
            label = font_renderer.render("Computer Wins!", 1, (255, 255, 255))
            screen.blit(label, (200, 600))
            return 1
    if 0 not in Board:
        label = font_renderer.render("Draw", 1, (255, 255, 255))
        screen.blit(label, (275, 610))
        return 10
    return 0
def Computer(Player,Board,Winner):
    if Player == -1 and Winner==0:
        depth = len(empty_cells(Board))
        move = minimax(Board, depth, -10000,10000,-1)
        #move = minimax(Board, depth,-1)
        X, Y = move[0], move[1]
        Board[X,Y]=-1
        Comp_Center = [100 + Y * 200,100 + X * 200]
        Draw_Shapes(Comp_Center, Player)
        return 1
def empty_cells(Board):
    cells = []
    for x, row in enumerate(Board):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells
def minimax(Board, depth, alpha, beta, player):
    if player == -1:
        best = [-1, -1, -10000]
    else:
        best = [-1, -1, +10000]
    if depth == 0 or Win(Board)!=0:
        Score = (-1)*Win(Board)
        return [-1, -1, Score]
    for cell in empty_cells(Board):
        x, y = cell[0], cell[1]
        Board[x,y] = player
        score = minimax(Board, depth - 1, alpha, beta, (-1)*player)
        Board[x,y] = 0
        score[0], score[1] = x, y
        if player == -1:
            if score[2] > best[2]:
                best = score
                alpha = max(score[2],alpha)
                if beta <= alpha:
                    break
        else:
            if score[2] < best[2]:
                best = score
                beta = min(score[2], beta)
                if beta <= alpha:
                    break
    return best

draw_board()
game_over=False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if Player ==1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                Player = Position(Board,Player,Winner)
                Winner = Final_Winner(Board)
        elif Player == -1:
            time.sleep(1)
            Player = Computer(Player, Board,Winner)
            Winner = Final_Winner(Board)
    pygame.display.update()
