from queue import Queue
import os
import random
import time
import graphic
import pygame

WIDTH, HEIGHT = 750, 500

EMPTY = 0
WALL = 1
FOOD = 2
GHOST = 3

DEAD = -1   # Collide with a ghost
RUNNING = 0
WIN = 1     # Collects all food to win

def read_input_file(input_file):
    with open(input_file, "r") as file:
        N, M = map(int, file.readline().split())
        graph = [list(map(int, file.readline().split())) for _ in range(N)]
        start_x, start_y = map(int, file.readline().split())

    return N, M, graph, start_x, start_y

def write_result_to_file(file_path, result):
    if not os.path.exists('./results'):
        os.makedirs('./results')
    with open(file_path, 'w') as file:
        file.write(result)

def is_valid_move(x, y, N, M, graph, is_ghost=0):
    return 0 <= x < N and 0 <= y < M and graph[x][y] != WALL and ((graph[x][y] != GHOST) or is_ghost)

def get_adjacent_tiles(x, y, N, M, graph, is_ghost=0):
    adjacent_tiles = []
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    for i in range(4):
        new_x, new_y = x + dx[i], y + dy[i]
        if is_valid_move(new_x, new_y, N, M, graph, is_ghost):
            adjacent_tiles.append((new_x, new_y))

    return adjacent_tiles

def bfs_with_visibility_limit(graph, start_x, start_y, target_x, target_y, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    queue = Queue()
    queue.put((start_x, start_y, 0))
    visited[start_x][start_y] = True
    parent = {(start_x, start_y): None}

    while not queue.empty():
        x, y, visibility = queue.get()

        if x == target_x and y == target_y:
            path = []
            current = (x, y)
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        if visibility >= 3:
            continue

        for adj_x, adj_y in get_adjacent_tiles(x, y, N, M, graph):
            if not visited[adj_x][adj_y]:
                queue.put((adj_x, adj_y, visibility + 1))
                visited[adj_x][adj_y] = True
                parent[(adj_x, adj_y)] = (x, y)
                
def bfs(graph, start_x, start_y, target_x, target_y, N, M, is_ghost=0):
    visited = [[False for _ in range(M)] for _ in range(N)]
    queue = Queue()
    queue.put((start_x, start_y))
    visited[start_x][start_y] = True
    parent = {(start_x, start_y): None}

    while not queue.empty():
        x, y = queue.get()

        if x == target_x and y == target_y:
            path = []
            current = (x, y)
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]
        
        
        for adj_x, adj_y in get_adjacent_tiles(x, y, N, M, graph, is_ghost):
            if not visited[adj_x][adj_y]:
                queue.put((adj_x, adj_y))
                visited[adj_x][adj_y] = True
                parent[(adj_x, adj_y)] = (x, y)

    return None  # No path to food

def find_nearest_food(graph, start_x, start_y, N, M):
    nearest_food = None
    min_distance = float('inf')

    for i in range(N):
        for j in range(M):
            if graph[i][j] == 2:
                distance = abs(i - start_x) + abs(j - start_y)
                if distance < min_distance:
                    min_distance = distance
                    nearest_food = (i, j)

    return nearest_food

def calculate_game_points(path_length, food_collected):
    movement_penalty = path_length

    food_reward = food_collected * 20

    game_points = food_reward - movement_penalty

    return game_points

class Game:
    def __init__(self, filepath):
        self.N, self.M, self.graph, x, y = read_input_file(filepath)
        self.game_points = 0
        self.game_state = RUNNING
        self.foods = []

        for row in range(self.N):
            for col in range(self.M):
                if(self.graph[row][col] == FOOD):
                    self.foods.append((row, col))
                    
        self.ghosts = []
        for row in range(self.N):
            for col in range(self.M):
                if self.graph[row][col] == GHOST:
                    self.ghosts.append((row, col))    
        
        self.pacman = (x, y)
        
    def play_game_level_1(self):
        self.game_points = 0
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        while True:
            nearest_food = find_nearest_food(self.graph, self.pacman[0], self.pacman[1], self.N, self.M)
            if nearest_food is None:
                self.game_state = WIN
                break

            path = bfs(self.graph, self.pacman[0], self.pacman[1], nearest_food[0], nearest_food[1], self.N, self.M)
            if path is None or len(path) < 2:
                print("No path to food!")
                self.game_state = DEAD
                return

            # Subtract 1 points for every move
            self.game_points -= 1
            # Move pacman 1 step
            self.pacman = path[1]
            
            # If pacman ate the food
            if(self.pacman == (nearest_food[0], nearest_food[1])):
                self.game_points += 20
                
            self.graph[self.pacman[0]][self.pacman[1]] = 0

            graphic.draw_board(self.pacman[0], self.pacman[1], self.graph, self.screen, HEIGHT, WIDTH)
            pygame.display.flip()
            time.sleep(1)

        return self.game_points

    def play_game_level_2(self):
        self.game_points = 0
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        while True:
            nearest_food = find_nearest_food(self.graph, self.pacman[0], self.pacman[1], self.N, self.M)
            if nearest_food is None:
                self.game_state = WIN
                break

            path = bfs(self.graph, self.pacman[0], self.pacman[1], nearest_food[0], nearest_food[1], self.N, self.M)
            if path is None or len(path) < 2:
                print("No path to food!")
                self.game_state = DEAD
                break

            # Subtract 1 points for every move
            self.game_points -= 1
            # Move pacman 1 step
            self.pacman = path[1]
            
            # If pacman ate the food
            if(self.pacman == (nearest_food[0], nearest_food[1])):
                self.game_points += 20
                
            self.graph[self.pacman[0]][self.pacman[1]] = 0

            graphic.draw_board(self.pacman[0], self.pacman[1], self.graph, self.screen, HEIGHT, WIDTH)
            pygame.display.flip()
            time.sleep(1)
           
        return self.game_points

    def play_game_level_3(self):
        self.game_points = 0
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])

        while True:
            nearest_food = find_nearest_food(self.graph, self.pacman[0], self.pacman[1], self.N, self.M)
            if nearest_food is None:
                self.game_state = WIN
                break
                
            for i, ghost in enumerate(self.ghosts):
                ghost_x, ghost_y = ghost
                self.graph[ghost_x][ghost_y] = 0
                adj_tiles = get_adjacent_tiles(
                    ghost[0],
                    ghost[1],
                    self.N,
                    self.M,
                    self.graph,
                    is_ghost=True
                )
                new_x, new_y = random.choice(adj_tiles)
                self.ghosts[i] = (new_x, new_y)
                self.graph[new_x][new_y] = GHOST
                
            path = bfs_with_visibility_limit(self.graph, self.pacman[0], self.pacman[1],
                                            nearest_food[0], nearest_food[1], self.N, self.M)
            if path is None or len(path) < 2:
                print("No path to food!")
                self.game_state = DEAD
                break

            # Subtract 1 points for every move
            self.game_points -= 1
            # Move pacman 1 step
            self.pacman = path[1]
            
            # If pacman ate the food
            if(self.pacman == (nearest_food[0], nearest_food[1])):
                self.game_points += 20
                
            self.graph[self.pacman[0]][self.pacman[1]] = 0

            graphic.draw_board(self.pacman[0], self.pacman[1], self.graph, self.screen, HEIGHT, WIDTH)
            pygame.display.flip()
            time.sleep(1)

        return self.game_points

    def play_game_level_4(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        while self.game_state == RUNNING:
            self.graph[self.pacman[0]][self.pacman[1]] = 0
            if len(self.foods) == 0:
                self.game_state = WIN
                break
            
            # Each ghost find the shortest path to Pacman
            for i, ghost in enumerate(self.ghosts):
                ghost_x, ghost_y = ghost
                if (ghost_x, ghost_y) in self.foods:
                    self.graph[ghost_x][ghost_y] = FOOD
                else:
                    self.graph[ghost_x][ghost_y] = 0
                ghost_path = bfs(self.graph, ghost_x, ghost_y, self.pacman[0], self.pacman[1], self.N, self.M, is_ghost=True)
                if len(ghost_path) >= 2:
                    # Ghost take a step
                    ghost = ghost_path[1]
                    self.graph[i] = ghost
                    self.graph[ghost[0]][ghost[1]] = GHOST
            
            # Pacman find shortest path to clostest food
            pacman_path = []
            for food in self.foods:
                print(food, self.pacman)
                pacman_path.append(bfs(self.graph, self.pacman[0], self.pacman[1], food[0], food[1], self.N, self.M, is_ghost=False))
            
            valid_path = [path for path in pacman_path if path]
            closest_food = min(valid_path, key=len, default=[]) if pacman_path else None
            
            if len(closest_food) <= 1:
                self.game_state = DEAD
                break
                
            # Pacman move to that food
            self.pacman = closest_food[1]
            self.game_points -= 1
            self.graph[self.pacman[0]][self.pacman[1]] = 5
            
            # Eat the food if pacman is at the food
            if self.pacman in self.foods:
                self.foods.remove(self.pacman)
                self.game_points += 20
                
            graphic.draw_board(self.pacman[0], self.pacman[1], self.graph, self.screen, HEIGHT, WIDTH)    
            pygame.display.flip()
            time.sleep(1)

        return self.game_points, self.game_state

    def save_result(self, level):
        if self.game_state == WIN:
            game_result = 'WIN'
        else:
            game_result = 'DEAD'
            
        result = f"Level {level}:\n"
        result += "\n".join(" ".join(str(cell) for cell in row) for row in self.graph)
        result += "\n\n" 
        result += f"Game points: {self.game_points}\n"
        result += f"Game result: {game_result}\n"
        output_file = f"./results/result{level}.txt"
        write_result_to_file(output_file, result)