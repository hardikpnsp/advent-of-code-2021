lines = []

with open('input.txt') as f:
    while(line := f.readline()):
        lines.append(line.strip())

pair = {
    '>': '<',
    ']': '[',
    ')': '(',
    '}': '{'
}

score = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

counts = {
    ')': 0,
    ']': 0,
    '}': 0,
    '>': 0,
}

completion_scores = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

completion_score = []

for line in lines:
    stack = []
    cs = 0
    for c in line:
        if not stack:
            if c in pair:
                counts[c] += 1
                break
            else:
                stack.append(c)
        elif c in pair:
            if stack[-1] == pair[c]:
                stack.pop()
            else:
                counts[c] += 1
                break
        else:
            stack.append(c)
    else:
        for c in reversed(stack):
            cs *= 5
            cs += completion_scores[c]
        completion_score.append(cs)

print(sum([score[c] * counts[c] for c in counts.keys()]))

print(sorted(completion_score)[len(completion_score)//2])