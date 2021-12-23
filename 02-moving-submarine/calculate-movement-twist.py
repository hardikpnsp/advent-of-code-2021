commands = []

with open('./input-2.txt') as f:
    while(line := f.readline()):
        commands.append(line.split(" "))

commands = map(lambda x: (x[0], int(x[1])), commands)

horizontal = 0
depth = 0
aim = 0

for direction, val in commands:
    match direction:
        case "forward":
            horizontal += val
            depth += aim * val
        case "down":
            aim += val
        case "up":
            aim -= val

print((horizontal, depth))
print(horizontal * depth)