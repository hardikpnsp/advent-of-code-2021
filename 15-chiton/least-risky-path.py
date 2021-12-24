grid = []
with open("./input.txt") as f:
    while(line := f.readline()):
        grid.append(list(map(int, line.strip())))

shortest_distance = 1000000

dircetions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def in_bound(i, j):
    if i >= 0 and j >= 0 and i < len(grid) and j < len(grid[i]):
        return True
    else:
        return False

distance_table = [[1000000 for _ in range(len(grid[0]))] for _ in range(len(grid))]

def backtrack(x, y, current_distance):
    global shortest_distance

    if x == len(grid) - 1 and y == len(grid[0]) - 1:
        shortest_distance = distance_table[len(grid)-1][len(grid[0])-1]

    for i, j in dircetions:
        l, m = x+i, y+j

        if in_bound(l, m):
            distance = current_distance + grid[l][m]

            if distance < distance_table[l][m] and distance < shortest_distance:
                distance_table[l][m] = distance
                backtrack(l, m, distance)
# solution 1
backtrack(0, 0, 0)

print(distance_table[len(grid)-1][len(grid[0])-1])

distance_table = [[1000000 for _ in range(len(grid[0]) * 5)] for _ in range(len(grid) * 5)]

shortest_distance = 1000000

def row_to_5x(row):
    result = row
    new_row = []
    for _ in range(1, 5):
        for i in row:
            i = i + 1
            if i > 9:
                i = 1
            new_row.append(i)
        result.extend(new_row)
        row = new_row
        new_row = []

    return result

grid5x = [row_to_5x(row) for row in grid]

grid_len = len(grid5x)

def row_to_new_row(row):
    return list(map(lambda x: 1 if x >= 9 else x + 1, row))

for j in range(4):
    for i in range(grid_len):
        index = i + (grid_len * j)
        grid5x.append(row_to_new_row(grid5x[index]))

grid = grid5x

import sys
x=1500
sys.setrecursionlimit(x)

# solution 2
backtrack(0, 0, 0)

print(shortest_distance)

# Took more than 30 mins, can try a different approach later