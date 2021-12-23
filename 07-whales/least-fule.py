crabs = []
with open('input.txt') as f:
    crabs = list(map(int, f.readline().strip().split(",")))


from collections import Counter
crab_counts = Counter(crabs)
print(crab_counts)

min_fule = 1000000000000000

min_dis = min(crabs)
max_dis = max(crabs)

for x in range(min_dis, max_dis+1):
    fule = 0
    for k, v in crab_counts.items():
        distance = abs(k - x)
        fule_expenditure = (distance * (distance + 1)) // 2
        fule += fule_expenditure * v
    if fule < min_fule:
        min_fule = fule

print(min_fule)