input_lines = []

with open("./input.txt") as f:
    while line := f.readline():
        input_lines.append(line.strip().split(" -> "))

lines = list(
    map(
        lambda x: tuple(
            [tuple(map(int, x[0].split(","))), tuple(map(int, x[1].split(",")))]
        ),
        input_lines,
    )
)


def extract_largest_x(point_pair):
    p1, p2 = point_pair
    x1, _ = p1
    x2, _ = p2
    return max(x1, x2)


def extract_largest_y(point_pair):
    p1, p2 = point_pair
    _, y1 = p1
    _, y2 = p2
    return max(y1, y2)

max_x = max(map(extract_largest_x, lines))
max_y = max(map(extract_largest_y, lines))

grid = [[0] * (max_x + 1) for _ in range(max_y + 1)]

for line in lines:
    p1, p2 = line
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2:
        for i in range(min(y1, y2), max(y1, y2) + 1):
            grid[i][x1] += 1
    elif y1 == y2:
        for i in range(min(x1, x2), max(x1, x2) + 1):
            grid[y1][i] += 1
    else:
        # 45 degree
        x_update = -1 if x1 > x2 else 1
        y_update = -1 if y1 > y2 else 1

        while(x1 != x2 and y1 != y2):
            grid[y1][x1] += 1
            x1 += x_update
            y1 += y_update

        grid[y2][x2] += 1


answer = 0

for row in grid:
    for point in row:
        if point >= 2:
            answer += 1

print(answer)