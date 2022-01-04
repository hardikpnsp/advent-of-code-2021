from functools import cache

div_z = []
add_y = []
add_x = []


def read_monad_instructions():
    monad_instructions = []
    with open("input.txt") as f:
        while line := f.readline():
            monad_instructions.append(tuple(line.strip().split(" ")))

    for i in range(4, len(monad_instructions), 18):
        div_z.append(int(monad_instructions[i][2]))
    for i in range(5, len(monad_instructions), 18):
        add_x.append(int(monad_instructions[i][2]))
    for i in range(15, len(monad_instructions), 18):
        add_y.append(int(monad_instructions[i][2]))
    return monad_instructions


@cache
def calculate(w, index, z_mod_26):
    x = z_mod_26 + add_x[index]
    if x == w:
        x = 0
    else:
        x = 1

    return (25 * x) + 1, (w + add_y[index]) * x


def process_digit(i, w, z):
    mul, add = calculate(w, i, z % 26)
    z //= div_z[i]
    z *= mul
    z += add
    return z


@cache
def model_number(index=0, z=0, largest=True):
    if index == 14:
        if z == 0:
            return []
        else:
            return None

    r = range(9, 0, -1) if largest else range(1, 10)

    for w in r:
        new_z = process_digit(index, w, z)
        ans = model_number(index + 1, new_z, largest=largest)
        if ans is not None:
            return [w] + ans

    return None


if __name__ == "__main__":
    monad_instructions = read_monad_instructions()
    largest_number = model_number()
    print(f'Part 1: Largest model number: {"".join(map(str, largest_number))}')
    smallest_number = model_number(largest=False)
    print(f'Part 2: Smallest model number: {"".join(map(str, smallest_number))}')

