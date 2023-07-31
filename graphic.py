import pygame
import sys
import Group_7 as g
import time

# Khởi tạo Pygame
pygame.init()

# Các hằng số màn hình
WIDTH, HEIGHT = 750, 500
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
fps = 60

def draw_board(pac_x, pac_y, board):
    screen.fill((0,0,0))
    num1 = (HEIGHT)//20
    num2 = (WIDTH-250)//20
    for i in range (len(board)):
        for j in range (len(board[i])):
            if board[i][j] == 2:
                pygame.draw.circle(screen,'white', (j * num2 + (0.5*num2), i*num1 +(0.5*num1)), 4)
            if board[i][j] == 1:
                pygame.draw.rect(screen,'blue', (j * num2, i* num1, 23, 23))
            if (i, j) == (pac_x, pac_y):
                pygame.draw.circle(screen,'yellow', (j * num2 + (0.5*num2), i*num1 +(0.5*num1)), 10)

# run = True
# while run:
#     timer.tick(fps)
#     screen.fill('black')
#     draw_board(start_x, start_y, graph)
#     start_x+=1
#     time.sleep(1)

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

#     pygame.display.flip()
# pygame.quit()