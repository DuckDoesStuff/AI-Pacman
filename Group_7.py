from queue import Queue
import copy

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        N, M = map(int, file.readline().split())
        graph = []
        for _ in range(N):
            row = list(map(int, file.readline().split()))
            graph.append(row)
        start_x, start_y = map(int, file.readline().split())
    return N, M, graph, start_x, start_y

def is_valid_move(x, y, N, M, graph):
    return 0 <= x < N and 0 <= y < M and graph[x][y] != 1

def bfs(graph, start_x, start_y, food_x, food_y, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    queue = Queue()
    queue.put((start_x, start_y))
    visited[start_x][start_y] = True
    parent = {(start_x, start_y): None}

    while not queue.empty():
        x, y = queue.get()

        if x == food_x and y == food_y:
            path = []
            current = (x, y)
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]

        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]

        for i in range(4):
            new_x, new_y = x + dx[i], y + dy[i]
            if is_valid_move(new_x, new_y, N, M, graph) and not visited[new_x][new_y]:
                queue.put((new_x, new_y))
                visited[new_x][new_y] = True
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
        if path is None or len(path) < 2:
            print("No path to food!")
            return
        
        game_points += len(path) *20 - (len(path) - 1)
        start_x, start_y = path[1]
        
        graph[start_x][start_y] = 0
        food_count -= 1

    return game_points

def play_gameL4(graph, start_x, start_y, N, M):
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
            game_points += len(path) * 20 - (len(path) - 1)
            start_x, start_y = path[1]

        graph[food_x][food_y] = 0
        graph[start_x][start_y] = 0
        food_count -= 1
    
    return game_points


def write_result_to_file(file_path, result):
    with open(file_path, 'w') as file:
        file.write(result)

def display_game(graph):
    for row in graph:
        print(" ".join(str(cell) for cell in row))
    print()

def main():
    for i in range(1, 6):
        print("Map ", i)
        input_file = f"./maps/map{i}.txt"
        N, M, graph, start_x, start_y = read_input_file(input_file)

        result = f"Level {i}:\n"
        result += "\n".join(" ".join(str(cell) for cell in row) for row in graph)
        result += "\n\n"

        game_points = play_game(copy.deepcopy(graph), start_x, start_y, N, M)
        result += f"Game points: {game_points}\n"

        output_file = f"./results/result{i}.txt"
        write_result_to_file(output_file, result)
    
    

if __name__ == "__main__":
    main()
