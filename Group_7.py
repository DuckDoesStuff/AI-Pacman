from queue import Queue
import copy
import time

EMPTY = 0
WALL = 1
FOOD = 2
GHOST = 9
DEAD = -1   # Collide with a ghost
RUNNING = 0
WIN = 1     # Collects all food to win


def read_input_file(file_path):
    with open(file_path, 'r') as file:
        N, M = map(int, file.readline().split())
        graph = []
        for _ in range(N):
            row = list(map(int, file.readline().split()))
            graph.append(row)
        start_x, start_y = map(int, file.readline().split())
    return N, M, graph, start_x, start_y

def is_valid_move(x, y, N, M, graph, is_ghost=0):
    return 0 <= x < N and 0 <= y < M and graph[x][y] != WALL and ((graph[x][y] != GHOST) or is_ghost)

def bfs(graph, start_x, start_y, goal_x, goal_y, N, M, is_ghost=0):
    visited = [[False for _ in range(M)] for _ in range(N)]
    queue = Queue()
    queue.put((start_x, start_y))
    visited[start_x][start_y] = True
    parent = {(start_x, start_y): None}
    
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]
    
    while not queue.empty():
        x, y = queue.get()
        visited[x][y] = True

        if x == goal_x and y == goal_y:
            path = []
            current = (x, y)
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for i in range(4):
            new_x, new_y = x + dx[i], y + dy[i]
            if is_valid_move(new_x, new_y, N, M, graph, is_ghost) and not visited[new_x][new_y]:
                queue.put((new_x, new_y))
                parent[(new_x, new_y)] = (x, y)

    return None  # No path to food

def play_game(graph, start_x, start_y, N, M):
    food_count = sum(row.count(2) for row in graph)
    game_points = 0

    while food_count > 0:
        food_x, food_y = None, None
        for i in range(N):
            for j in range(M):
                if graph[i][j] == 2:
                    food_x, food_y = i, j
                    break
            if food_x is not None:
                break

        path = bfs(graph, start_x, start_y, food_x, food_y, N, M)
        if path is not None and len(path) >= 2:
            # print("No path to food!")
            game_points += 20 - (len(path) - 1)
            start_x, start_y = path[1]
        
        graph[food_x][food_y] = 0
        graph[start_x][start_y] = 0
        food_count -= 1

    return game_points

def play_gameL4(graph, start_x, start_y, N, M):
    game_points = 0
    game_state = RUNNING
    
    foods = []
    for row in range(N):
        for col in range(M):
            if graph[row][col] == FOOD:
                foods.append((row, col))
    
    ghosts = []
    for row in range(N):
        for col in range(M):
            if graph[row][col] == GHOST:
                ghosts.append((row, col))

    pacman = (start_x, start_y)
    while game_state == RUNNING:
        graph[pacman[0]][pacman[1]] = 0
        if len(foods) == 0:
            game_state = WIN
            break
        
        # Each ghost find the shortest path to Pacman
        for i, ghost in enumerate(ghosts):
            ghost_x, ghost_y = ghost
            if (ghost_x, ghost_y) in foods:
                graph[ghost_x][ghost_y] = FOOD
            else:
                graph[ghost_x][ghost_y] = 0
            ghost_path = bfs(graph, ghost_x, ghost_y, pacman[0], pacman[1], N, M, is_ghost=True)
            if len(ghost_path) >= 2:
                # Ghost take a step
                ghost = ghost_path[1]
                ghosts[i] = ghost
                graph[ghost[0]][ghost[1]] = GHOST
        
        # Pacman find shortest path to clostest food
        pacman_path = []
        for food in foods:
            pacman_path.append(bfs(graph, pacman[0], pacman[1], food[0], food[1], N, M, is_ghost=False))
        
        valid_path = [path for path in pacman_path if path]
        closest_food = min(valid_path, key=len, default=[]) if pacman_path else None
        
        if len(closest_food) <= 1:
            game_state = DEAD
            break
            
        # Pacman move to that food
        pacman = closest_food[1]
        game_points -= 1
        graph[pacman[0]][pacman[1]] = 5
        
        # Eat the food if pacman is at the food
        if pacman in foods:
            foods.remove(pacman)
            game_points += 20
            
        # display_game(graph)
        # time.sleep(3)
        
    # if game_state == WIN:
    #     print("Pacman ate all the food!")
    # elif game_state == DEAD:
    #     print("Pacman was captured by the ghosts")
    
    return game_points, game_state


def write_result_to_file(file_path, result):
    with open(file_path, 'w') as file:
        file.write(result)

def display_game(graph):
    for row in graph:
        print(" ".join(str(cell) for cell in row))
    print()

def main():
    # for i in range(1, 6):
    #     print("Map ", i)
    #     input_file = f"./maps/map{i}.txt"
    #     N, M, graph, start_x, start_y = read_input_file(input_file)

    #     result = f"Level {i}:\n"
    #     result += "\n".join(" ".join(str(cell) for cell in row) for row in graph)
    #     result += "\n\n"

    #     game_points = play_game(copy.deepcopy(graph), start_x, start_y, N, M)
    #     result += f"Game points: {game_points}\n"

    #     output_file = f"./results/result{i}.txt"
    #     write_result_to_file(output_file, result)
    N, M, graph, start_x, start_y = read_input_file('./maps/map10.txt')
    game_points, game_states = play_gameL4(copy.deepcopy(graph), start_x, start_y, N, M)
    if game_states == WIN:
        game_result = 'WIN'
    else:
        game_result = 'DEAD'
    result = f"Level {10}:\n"
    result += "\n".join(" ".join(str(cell) for cell in row) for row in graph)
    result += "\n\n" 
    result += f"Game points: {game_points}\n"
    result += f"Game result: {game_result}\n"
    output_file = f"./results/result{10}.txt"
    write_result_to_file(output_file, result)
    
    

if __name__ == "__main__":
    main()
