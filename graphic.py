import pygame

def draw_board(pac_x, pac_y, board, screen, height, width):
    screen.fill((0, 0, 0))
    num1 = (height)//20
    num2 = (width-250)//20
    for i in range (len(board)):
        for j in range (len(board[i])):
            if board[i][j] == 2:
                pygame.draw.circle(screen,'white', (j * num2 + (0.5*num2), i*num1 +(0.5*num1)), 4)
            if board[i][j] == 1:
                pygame.draw.rect(screen,'blue', (j * num2, i* num1, 23, 23))
            if (i, j) == (pac_x, pac_y):
                pygame.draw.circle(screen,'yellow', (j * num2 + (0.5*num2), i*num1 +(0.5*num1)), 10)