edges = []

with open('input.txt') as f:
    while(line := f.readline()):
        edges.append(tuple(line.strip().split("-")))

def is_small_cave(cave_name: str):
    return cave_name.islower()

from collections import defaultdict
from typing import DefaultDict
edge_map: DefaultDict[str, list[str]] = defaultdict(set)

for start, end in edges:
    edge_map[start].add(end)
    if start != "start":
        edge_map[end].add(start)

print(edge_map)

paths = []

def backtrack(current_edge, visited_small_caves, current_path):
    if current_edge == "end":
        paths.append(current_path[:])
        return

    for cave in edge_map[current_edge]:
        if is_small_cave(cave):
            if cave not in visited_small_caves:
                visited_small_caves.add(cave)
                current_path.append(cave)
                backtrack(cave, visited_small_caves.copy(), current_path)
                current_path.pop()
                visited_small_caves.remove(cave)
        else:
            current_path.append(cave)
            backtrack(cave, visited_small_caves.copy(), current_path)
            current_path.pop()

backtrack("start", set(["start"]), ["start"])

small_cave_at_most_once = 0

print(len(paths))

paths = []


def backtrack_small_cave_twice(current_edge, visited_small_caves, small_cave_twice, current_path):
    if current_edge == "end":
        paths.append(current_path[:])
        return

    for cave in edge_map[current_edge]:
        if is_small_cave(cave):
            if cave not in visited_small_caves:
                visited_small_caves.add(cave)
                current_path.append(cave)
                backtrack_small_cave_twice(cave, visited_small_caves.copy(), small_cave_twice, current_path)
                current_path.pop()
                visited_small_caves.remove(cave)
            elif not small_cave_twice and cave != "start" and cave != "end":
                current_path.append(cave)
                backtrack_small_cave_twice(cave, visited_small_caves.copy(), True, current_path)
                current_path.pop()
        else:
            current_path.append(cave)
            backtrack_small_cave_twice(cave, visited_small_caves.copy(), small_cave_twice, current_path)
            current_path.pop()

backtrack_small_cave_twice("start", set(["start"]), False, ["start"])


print(len(paths))
