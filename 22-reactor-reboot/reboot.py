from collections import defaultdict
from itertools import chain


def read_inputs():
    reboot_steps = []
    with open("./input.txt") as f:
        while line := f.readline():
            action, intervals = line.strip().split(" ")
            xr, yr, zr = tuple(map(lambda x: tuple(map(int, x.split("=")[1].split(".."))), intervals.split(",")))
            reboot_steps.append([action == "on", (xr, yr, zr)])
    return reboot_steps


def initialization(reboot_step, limit=50):
    _, bounds = reboot_step
    xr, yr, zr = bounds
    for a in chain(xr, yr, zr):
        if not -limit <= a <= limit:
            return False
    return True


def cube_volume(bounds):
    x1, x2 = bounds[0]
    y1, y2 = bounds[1]
    z1, z2 = bounds[2]
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1) * (abs(z2 - z1) + 1)


def overlaps(bounds1, bounds2):
    overlapping_cube_bounds = []
    for n1, n2 in zip(bounds1, bounds2):
        # if any dimension doesn't overlap -> the cubes don't overlap
        if n1[1] < n2[0] or n2[1] < n1[0]:
            return None
        bounds = (max(n1[0], n2[0]), min(n1[1], n2[1]))
        overlapping_cube_bounds.append(bounds)
    return tuple(overlapping_cube_bounds)


def count(reboot_steps):
    counts = defaultdict(int)
    for reboot_step in reboot_steps:
        switch, bounds = reboot_step
        updates = defaultdict(int)
        keys = set(counts.keys())
        # total cubes = sum of both cubes - overlapping cubes
        for cube in keys:
            if overlapping := overlaps(bounds, cube):
                updates[overlapping] -= counts[cube]
        if switch:
            updates[bounds] += 1
        for c in updates:
            counts[c] += updates[c]
    return counts


def main():
    reboot_steps = read_inputs()

    initialization_steps = filter(lambda x: initialization(x), reboot_steps)
    counts = count(initialization_steps)
    p1 = sum(map(lambda cube: cube_volume(cube) * counts[cube], counts))
    print(f"Part 1: {p1}")

    counts = count(reboot_steps)
    p2 = sum(map(lambda cube: cube_volume(cube) * counts[cube], counts))
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
