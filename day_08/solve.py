from collections import defaultdict
import itertools


antenna_coordinates = defaultdict(set)
map_size = None


with open('input') as infile:
    for x, line in enumerate(infile):
        for y, char in enumerate(line.strip()):
            if char.isalnum():
                antenna_coordinates[char].add((x, y))
            map_size = (x, y)

print(map_size)

def is_in_grid(coord):
    return (0 <= coord[0] <= map_size[0]) and (0 <= coord[1] <= map_size[1])

def solve_1():
    antinode_locations = set()
    for _, antennae in antenna_coordinates.items():
        for first, second in itertools.permutations(antennae, 2):
            difference = (second[0] - first[0], second[1] - first[1])
            antinode_location = (second[0] + difference[0], second[1] + difference[1])
            if is_in_grid(antinode_location):
                antinode_locations.add(antinode_location)
    print(len(antinode_locations))

def solve_2():
    antinode_locations = set()
    for _, antennae in antenna_coordinates.items():
        for first, second in itertools.permutations(antennae, 2):
            difference = (second[0] - first[0], second[1] - first[1])
            antinode_location = second
            while is_in_grid(antinode_location):
                antinode_locations.add(antinode_location)
                antinode_location = (antinode_location[0] + difference[0], antinode_location[1] + difference[1])
    print(len(antinode_locations))

solve_1()
solve_2()