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

N, M, graph, start_x, start_y = read_input_file('./maps/map10.txt')

ghosts = []
for row in range(N):
    for col in range(M):
        if graph[row][col] == 9:
            ghosts.append((row, col))
        