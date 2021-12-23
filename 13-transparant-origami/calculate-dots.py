dots = []
instructions = []

with open("./input.txt") as f:
    while(line := f.readline()):
        if line.startswith("fold"):
            instructions.append(line.strip().split(" ")[-1].split("="))
        elif not line.startswith('\n'):
            dot = [int(char) for char in line.strip().split(",")]
            dots.append(dot)

max_x = 0
max_y = 0
for x, y in dots:
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y

grid = [[0 for _ in range(max_x+1)] for _ in range(max_y+1)]

for x, y in dots:
    grid[y][x] = 1

def fold(axis, line, grid):
    y = len(grid)
    x = len(grid[0])

    if axis == "x":
        # fold left
        new_x = line
        for i in range(1, x-line):
            existing_x = new_x - i
            overlap_x = new_x + i
            for i in range(y):
                grid[i][existing_x] |= grid[i][overlap_x]


        new_grid = [row[:new_x] for row in grid]
        return new_grid

    else:
        # fold right
        new_y = line
        for i in range(1, y-line):
            existing_y = new_y - i
            overlap_y = new_y + i
            for i in range(x):
                grid[existing_y][i] |= grid[overlap_y][i]

        return grid[:new_y][:]


for axis, line in instructions:
    print((len(grid), len(grid[0])))
    grid = fold(axis, int(line), grid)
    print((len(grid), len(grid[0])))

def calculate_dots(grid):
    count = 0
    for row in grid:
        for cell in row:
            if cell == 1:
                count += 1
    return count

print(calculate_dots(grid))

for row in grid:
    s = ""
    for cell in row:
        if cell == 1:
            s += "#"
        else:
            s += "."
    print(s)