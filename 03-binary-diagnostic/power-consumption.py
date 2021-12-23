bits = []

with open('./input.txt') as f:
    while(line := f.readline()):
        bits.append(line.strip())

width = len(bits[0])

ones = [0] * width
zeroes = [0] * width

for bit in bits:
    for i, b in enumerate(bit):
        match b:
            case '1':
                ones[i] += 1
            case '0':
                zeroes[i] += 1

gamma_str = "".join(map(lambda x: '1' if x[0] > x[1] else '0', zip(ones, zeroes)))
epsilon_str = "".join(map(lambda x: '1' if x == '0' else '0', gamma_str))
gamma = int(gamma_str, 2)
epsilon = int(epsilon_str, 2)

print(gamma * epsilon)