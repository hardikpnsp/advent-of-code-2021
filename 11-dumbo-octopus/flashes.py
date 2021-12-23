grid = []

with open('input.txt') as f:
    while(line := f.readline()):
        grid.append(list(map(int, line.strip())))

from collections import deque
from functools import total_ordering


def simulate(grid):
    total_flashes = 0

    flash_queue = deque()

    # energy level of each octopus is increased by 1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] += 1

            # any octopus with energy greater than 9 flashes
            if grid[i][j] > 9:
                flash_queue.append((i, j))

    # for each flash, increases energy level of adjecent octopus by 1

    directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]

    def in_grid(i, j):
        if i >= 0 and j >= 0 and i < len(grid) and j < len(grid[i]):
            return True
        else:
            return False

    while(flash_queue):
        i, j = flash_queue.popleft()
        total_flashes += 1
        for m, n in directions:
            x, y = i + m, j + n
            if in_grid(x, y):
                # don't check already flashed ones
                if grid[x][y] < 10:
                    grid[x][y] += 1
                    # if energy level greater than 9, it also flashes
                    if grid[x][y] > 9:
                        flash_queue.append((x, y))

        # continue as long as new octopus keep flashing

    # any octopus that flashed has it's energy set to zero
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] > 9:
                grid[i][j] = 0

    return total_flashes

total_flashes = 0
for i in range(1000):
    flashes = simulate(grid)
    for row in grid:
        print(row)
    total_flashes += flashes
    if flashes == len(grid) * len(grid[0]):
        print("All octopus flashed at step: {}".format(i+1))
        input()
    print("After simulation {0}, Total Flashes: {1}".format(i+1, total_flashes))
