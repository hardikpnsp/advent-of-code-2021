initial_state = ""
rules = {}
with open("./input.txt") as f:
    initial_state = f.readline()
    f.readline()

    while(line := f.readline()):
        rule = line.strip().split(" -> ")
        rules[rule[0]] = rule[1]

print(rules)

def polymorph(initial_state):
    result = [initial_state[0]]
    first_char = initial_state[0]
    for c in initial_state[1:]:
        pair = first_char + c
        if pair in rules:
            insert = rules[pair]
            result.append(insert)
        result.append(c)
        first_char = c

    return "".join(result)

state = initial_state
for i in range(10):
    state = polymorph(state)
    # print(f"Step {i} completed, len of string {len(state)}")


from collections import Counter
from functools import cache

counts = Counter(state.strip())

print(counts)

print(max(counts.values()) - min(counts.values()))


"""
if AB -> X
then
AB after 40 steps = AX after 39 steps + XC after 39 steps, we can cache stuff for each pair

can't keep string of length 2188189693529 in memory, just store counts?

"""

@cache
def polymorph_pair(pair, step):
    # print(f"STEP: {step}; Working on pair: {pair}")
    counts = Counter(rules[pair])

    if step == 1:
        return counts


    if pair in rules:
        new_counts = polymorph_pair(pair[0] + rules[pair], step-1)
        for key, val in new_counts.items():
            counts[key] += val


        new_counts = polymorph_pair(rules[pair] + pair[1], step-1)
        for key, val in new_counts.items():
            counts[key] += val

    return counts

steps = 40
counts = Counter(initial_state.strip())
first_char = initial_state[0]
for char in initial_state[1:].strip():
    pair = first_char + char
    new_counts = polymorph_pair(pair.strip(), steps)
    print(new_counts)
    for key, val in new_counts.items():
        counts[key] += val
    first_char = char

print(counts)

print(max(counts.values()) - min(counts.values()))