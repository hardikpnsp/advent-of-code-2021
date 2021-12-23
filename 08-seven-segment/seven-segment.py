from collections import defaultdict

displays = []

with open("input.txt") as f:
    while line := f.readline():
        numbers, digits = line.split("|")
        numbers, digits = numbers.strip().split(" "), digits.strip().split(" ")
        displays.append((numbers, digits))

total = 0

seven_segments = {
    0: set(["a", "b", "c", "e", "f", "g"]),
    1: set(["c", "f"]),
    2: set(["a", "c", "d", "e", "g"]),
    3: set(["a", "c", "d", "f", "g"]),
    4: set(["b", "c", "d", "f"]),
    5: set(["a", "b", "d", "f", "g"]),
    6: set(["a", "b", "d", "e", "f", "g"]),
    7: set(["a", "c", "f"]),
    8: set(["a", "b", "c", "d", "e", "f", "g"]),
    9: set(["a", "b", "c", "d", "f", "g"]),
}

for numbers, display in displays:
    mapping = {}
    len_map = defaultdict(list)

    for num in numbers:
        len_map[len(num)].append(num)

    a = list(set(len_map[3][0]).difference(set(len_map[2][0])))[0]
    mapping[a] = 'a'

    bd = set(len_map[4][0]) - set(len_map[2][0])
    cf = set(len_map[2][0])

    for digit in len_map[5]:
        digit = set(digit)
        if len(cf.intersection(digit)) == 2:
            # digit is 3
            continue
        if len(cf.intersection(digit)) == 1:
            # digit is either 5 or 2
            if len(bd.intersection(digit)) == 2:
                # digit is 5
                f = list(cf.intersection(digit))[0]
                c = list(cf.difference(set([f])))[0]

                mapping[f] = 'f'
                mapping[c] = 'c'
            else:
                # digit is 3
                d = list(bd.intersection(digit))[0]
                b = list(bd.difference(set([d])))[0]

                mapping[d] = 'd'
                mapping[b] = 'b'

    for digit in len_map[6]:
        digit = set(digit)

        if len(cf.intersection(digit)) == 2 and len(bd.intersection(digit)) == 2:
            # digit is 9
            e = list(set(len_map[7][0]).difference(digit))[0]
            mapping[e] = 'e'

    g = list(set(len_map[7][0]).difference(set(mapping.keys())))[0]
    mapping[g] = 'g'

    def map_number(num: str):
        new_num = list(map(lambda c: mapping[c], num))
        return "".join(new_num)

    display = list(map(map_number, display))

    output = []

    for digit in display:
        for key, val in seven_segments.items():
            if set(digit) == val:
                output.append(key)

    total += int("".join(map(str, output)))
print(total)
