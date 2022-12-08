from pathlib import Path

grid_raw = Path('input.txt').read_text().splitlines()

grid = [[int(tree) for tree in row] for row in grid_raw]

def visible_side(lane):
    current_min = -1
    for i, tree in lane:
        if tree > current_min:
            yield i
            current_min = tree

def visible_grid():
    can_see = [[False] * len(row) for row in grid]
    for i, row in enumerate(grid):
        for j in visible_side(enumerate(row)):
            can_see[i][j] = True
        for j in visible_side(reversed(list(enumerate(row)))):
            can_see[i][j] = True
    for j in range(len(grid[0])):
        column = [(i, grid[i][j]) for i in range(len(grid))]
        for i in visible_side(column):
            can_see[i][j] = True
        for i in visible_side(reversed(column)):
            can_see[i][j] = True
    return can_see

def visible_count(can_see):
    return sum(1 for row in can_see for seen in row if seen is True)

def scenic_view_lane(current, lane):
    n = 0
    for tree in lane:
        n += 1
        if tree >= current:
            return n
    return n

def scenic_view_tree(i, j):
    current = grid[i][j]
    right = scenic_view_lane(current, grid[i][j+1:])
    left = scenic_view_lane(current, reversed(grid[i][:j]))
    column = [grid[i2][j] for i2 in range(len(grid))]
    down = scenic_view_lane(current, column[i+1:])
    up = scenic_view_lane(current, reversed(column[:i]))
    return right * left * down * up

def scenic_view():
    for i, row in enumerate(grid):
        for j in range(len(row)):
            yield scenic_view_tree(i, j)

print(visible_count(visible_grid()))
print(max(scenic_view()))