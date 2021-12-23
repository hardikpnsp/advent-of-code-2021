fish = []
with open('input.txt') as f:
    fish = list(map(int, f.readline().strip().split(",")))

print("Starting: {}".format(len(fish)))

from collections import Counter
fish_by_age = Counter(fish)

for x in range(256):
    temp = fish_by_age[0]
    for i in range(1, 9):
        fish_by_age[i-1] = fish_by_age[i]

    fish_by_age[6] += temp
    fish_by_age[8] = temp

print(fish_by_age)
print(sum(fish_by_age.values()))