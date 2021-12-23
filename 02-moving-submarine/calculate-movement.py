commands = []

with open('./input.txt') as f:
    while(line := f.readline()):
        commands.append(line.split(" "))

commands = map(lambda x: (x[0], int(x[1])), commands)

horizontal = 0
depth = 0

for direction, val in commands:
    match direction:
        case "forward":
            horizontal += val
        case "down":
            depth += val
        case "up":
            depth -= val

print((horizontal, depth))
print(horizontal * depth)