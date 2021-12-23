depths = []

with open('./input.txt') as f:
    while(line := f.readline()):
        depths.append(int(line))

increasing = 0
for i in range(1, len(depths)):
    if depths[i-1] < depths[i]:
        increasing += 1

print(increasing)