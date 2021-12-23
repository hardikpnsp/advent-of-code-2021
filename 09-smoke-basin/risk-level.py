height_map = []

with open('input.txt') as f:
    while(line := f.readline()):
        height_map.append(list(map(int, line.strip())))

directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

low_points = []

def bound_check(x, y):
    if x >= 0 and y >= 0 and x < len(height_map) and y < len(height_map[x]):
        return True
    else:
        return False

def check_low_point(i, j):
    for ii, jj in directions:
        x, y = i + ii, j + jj
        if bound_check(x, y):
            if height_map[x][y] <= height_map[i][j]:
                return False

    return True

for i in range(len(height_map)):
    for j in range(len(height_map[i])):
        if check_low_point(i, j):
            low_points.append((i, j))


from collections import deque
from functools import reduce

def bfs(i, j):
    nodes = deque([(i, j)])
    size = 0
    while(nodes):
        node = nodes.popleft()
        l, m = node
        height_map[l][m] = -1
        size += 1
        for ii, jj in directions:
            x, y = l + ii, m + jj
            if bound_check(x, y):
                if height_map[x][y] > 0 and height_map[x][y] < 9:
                    height_map[x][y] = -1
                    nodes.append((x, y))

    return size


basins = []

for i, j in low_points:
    basin_size = bfs(i, j)
    basins.append(basin_size)

print(reduce(lambda x, y: x * y, sorted(basins, reverse=True)[:3]))