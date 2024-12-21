import functools
import itertools

with open('input') as infile:
    lines = infile.read().strip().split('\n')

map_first = [
    '789',
    '456',
    '123',
    ' 0A'
]
coordinates_first = {}
for x, line in enumerate(map_first):
    for y, char in enumerate(line):
        coordinates_first[char] = (x, y)

map_other = [
    ' ^A',
    '<v>',
]
coordinates_other = {}
for x, line in enumerate(map_other):
    for y, char in enumerate(line):
        coordinates_other[char] = (x, y)

def type_sequence(line, coordinate_map=coordinates_first):
    location = coordinate_map['A']
    combination = []
    for first_char in line:
        destination = coordinate_map[first_char]
        
        # 2 options: first horizontal, then vertical
        # or, first vertical, then horizontal
        difference = (destination[0] - location[0], destination[1] - location[1])
        current_combinations = set()
        forbidden = coordinate_map[' ']
        # check if first vertical, then horizontal is ok
        if not (location[1] == forbidden[1] and destination[0] == forbidden[0]):
            # ok
            current_combinations.add(
                'v^'[difference[0] < 0]*abs(difference[0])
                + '><'[difference[1] < 0]*abs(difference[1])
                + 'A'
            )
        if not (destination[1] == forbidden[1] and location[0] == forbidden[0]):
            # ok
            current_combinations.add(
                '><'[difference[1] < 0]*abs(difference[1])
                + 'v^'[difference[0] < 0]*abs(difference[0])
                + 'A'
            )
        combination.append(current_combinations)
        location = destination
    return combination

@functools.cache
def cost_of_atom(atom, level=0, first_map=False):
    if level <= 0:
        shortest_len = float('inf')
        combinations = type_sequence(atom, coordinate_map=coordinates_other)
        for c in itertools.product(*combinations):
            instruction = ''.join(c)
            if len(instruction) < shortest_len:
                shortest_len = len(instruction)
        return shortest_len
    else:
        total = 0
        coordinate_map = coordinates_first if first_map else coordinates_other
        for possible_set in type_sequence(atom, coordinate_map=coordinate_map):
            cheapest = float('inf')
            for atom in possible_set:
                cheapest = min(cheapest, cost_of_atom(atom, level=level-1))
            total += cheapest
        return total


first = 0
second = 0
for line in lines:
    sequence_length_2 = cost_of_atom(line, level=2, first_map=True)
    sequence_length_25 = cost_of_atom(line, level=25, first_map=True)
    num = int(line[:-1])
    first += sequence_length_2 * num
    second += sequence_length_25 * num
print(first)
print(second)
