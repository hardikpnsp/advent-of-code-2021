def read_input():
    cucumbers = []
    with open("input.txt") as f:
        while (line := f.readline()):
            row = [char for char in line.strip()]
            cucumbers.append(row)
    return cucumbers


def simulate(grid):
    move_east = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            next_j = (j + 1) % len(grid[0])
            if grid[i][j] == ">" and grid[i][next_j] == ".":
                move_east.append((i, j))

    for i, j in move_east:
        next_j = (j + 1) % len(grid[0])
        grid[i][j] = "."
        grid[i][next_j] = ">"

    move_south = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            next_i = (i + 1) % len(grid)
            if grid[i][j] == "v" and grid[next_i][j] == ".":
                move_south.append((i, j))

    for i, j in move_south:
        next_i = (i + 1) % len(grid)
        grid[i][j] = "."
        grid[next_i][j] = "v"

    return len(move_east) + len(move_south)


def main():
    grid = read_input()
    step = 1
    while simulate(grid) > 0:
        step += 1
    return step


if __name__ == "__main__":
    print(f"Part 1: {main()}")
