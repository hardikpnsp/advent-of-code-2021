depths = []

with open('./input-2.txt') as f:
    while(line := f.readline()):
        depths.append(int(line))


for i in range(len(depths)-2):
    depths[i] += depths[i+1] + depths[i+2]

increasing = 0
for i in range(1, len(depths)-2):
    if depths[i-1] < depths[i]:
        increasing += 1

print(increasing)