from pathlib import Path
from collections import deque
from itertools import chain

grid = Path('input.txt').read_text().splitlines()

directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]

def to_height(letter):
    match letter:
        case 'S':
            return 'a'
        case 'E':
            return 'z'
        case _:
            return letter

def edges_single(i, j):
    for d in directions:
        x = j + d[0]
        y = i + d[1]
        if x < 0 or x >= len(grid[0]):
            continue
        if y < 0 or y >= len(grid):
            continue
        node = to_height(grid[i][j])
        neighbour = to_height(grid[y][x])
        if neighbour <= node or ord(neighbour) == ord(node)+1:
            yield (x, y)

def get_edges():
    for i, row in enumerate(grid):
        for j in range(len(row)):
            yield ((j, i), list(edges_single(i, j)))

graph = {node: edges for node, edges in get_edges()}

def find_letter_position(letter):
    for i, row in enumerate(grid):
        for j, node in enumerate(row):
            if node == letter:
                yield (j, i)

end = next(find_letter_position('E'))

def find_shortest_path(start):
    explored = set()
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            for neighbour in neighbours:
                next_path = list(path)
                next_path.append(neighbour)
                queue.append(next_path)
                if neighbour == end:
                    return next_path
            explored.add(node)
    return False

def find_all_shortest_paths():
    for start in chain(find_letter_position('S'), find_letter_position('a')):
        path = find_shortest_path(start)
        if not path:
            continue
        yield path

def find_shortest_path_2():
    shortest_path = None
    for path in find_all_shortest_paths():
        if shortest_path is None or len(path) < len(shortest_path):
            shortest_path = path
    return shortest_path

def visualize_path(path):
    canvas = [list(row) for row in grid]
    for x, y in path:
        canvas[y][x] = '.'
    return '\n'.join(''.join(row) for row in canvas)

start = next(find_letter_position('S'))
shortest_path = find_shortest_path(start)
print(visualize_path(shortest_path))
print(len(shortest_path)-1)
print('---')
shortest_path_2 = find_shortest_path_2()
print(visualize_path(shortest_path_2))
print(len(shortest_path_2) - 1)