from collections import defaultdict


def transform(x, y, z, transform_type):
    if transform_type == 0:
        return x, y, z
    elif transform_type == 1:
        # 90 left rotation from z axis
        return -y, x, z
    elif transform_type == 2:
        # 180 left rotation from z axis
        return -x, -y, z
    elif transform_type == 3:
        # 270 left rotation from z axis
        return y, -x, z
    elif transform_type == 4:
        # bring x to z and then do all 4 previous rotations
        return transform(-z, y, x, 0)
    elif transform_type == 5:
        return transform(-z, y, x, 1)
    elif transform_type == 6:
        return transform(-z, y, x, 2)
    elif transform_type == 7:
        return transform(-z, y, x, 3)
    elif transform_type == 8:
        # bring y to z and then do 4 rotations
        return transform(x, -z, y, 0)
    elif transform_type == 9:
        return transform(x, -z, y, 1)
    elif transform_type == 10:
        return transform(x, -z, y, 2)
    elif transform_type == 11:
        return transform(x, -z, y, 3)
    elif transform_type == 12:
        # bring -x to z and then do 4 rotations
        return transform(z, y, -x, 0)
    elif transform_type == 13:
        return transform(z, y, -x, 1)
    elif transform_type == 14:
        return transform(z, y, -x, 2)
    elif transform_type == 15:
        return transform(z, y, -x, 3)
    elif transform_type == 16:
        # bring -y to z and then do 4 rotations
        return transform(x, z, -y, 0)
    elif transform_type == 17:
        return transform(x, z, -y, 1)
    elif transform_type == 18:
        return transform(x, z, -y, 2)
    elif transform_type == 19:
        return transform(x, z, -y, 3)
    elif transform_type == 20:
        # bring -z to z and do 4 rotations
        return transform(-x, y, -z, 0)
    elif transform_type == 21:
        return transform(-x, y, -z, 1)
    elif transform_type == 22:
        return transform(-x, y, -z, 2)
    elif transform_type == 23:
        return transform(-x, y, -z, 3)


def read_file():
    scanners = []
    with open("./input.txt") as f:
        current_scanner = []
        while line := f.readline():
            if line.startswith("\n"):
                scanners.append(current_scanner)
                current_scanner = []
            elif line.startswith("---"):
                continue
            else:
                current_scanner.append(tuple(map(int, line.strip().split(","))))
        if current_scanner:
            scanners.append(current_scanner)

    return scanners


def relative_distance(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return x1 - x2, y1 - y2, z1 - z2


def invert_point(x, y, z):
    return -x, -y, -z


def add_points(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return x1 + x2, y1 + y2, z1 + z2


def all_possible_relative_distances(all_beacons, test_scanner, rotation):
    offsets = defaultdict(int)
    for beacon in all_beacons:
        for point in test_scanner:
            rotated_point = transform(*point, rotation)
            offset = relative_distance(rotated_point, beacon)
            offsets[offset] += 1

    return offsets


def part1(scanners):
    all_beacons = set(scanners.pop(0))
    scanner_coordinates = [(0, 0, 0)]

    while scanners:
        test_scanner = scanners.pop(0)
        match = False

        for rotation in range(24):

            offsets = all_possible_relative_distances(all_beacons, test_scanner, rotation)

            for offset, count in offsets.items():
                # if 12 relative distances match, we can assume that those beacons are common
                if count >= 12:
                    match = True
                    scanner = invert_point(*offset)
                    scanner_coordinates.append(scanner)
                    for point in test_scanner:
                        point = transform(*point, rotation)
                        all_beacons.add(add_points(point, scanner))
                    break

            if match:
                break

        if not match:
            scanners.append(test_scanner)

    print(f"Part 1: {len(all_beacons)}")
    return scanner_coordinates


def manhattan_distance(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def part2(scanner_coordinates):
    max_scanner_distance = 0
    for p1 in scanner_coordinates:
        for p2 in scanner_coordinates:
            distance = manhattan_distance(p1, p2)
            if distance > max_scanner_distance:
                max_scanner_distance = distance
    print(f"Part 2: {max_scanner_distance}")


if __name__ == "__main__":
    scanners = read_file()
    scanner_coordinates = part1(scanners)
    part2(scanner_coordinates)
