from collections import defaultdict
from functools import reduce

# parse
connections = defaultdict(set)
with open('input') as infile:
    for line in infile:
        first, second = line.strip().split('-')
        connections[first].add(second)
        connections[second].add(first)

# part 1
three_computer_sets = set()
for f in connections:
    if not f.startswith('t'):
        continue
    for s in connections[f]:
        for t in connections[f]:
            if len({f, s, t}) != 3:
                continue
            if t not in connections[s]:
                continue
            three_computer_sets.add(frozenset([f, s, t]))
print(len(three_computer_sets))

# part 2
current_generation = {frozenset([computer]) for computer in connections}
while True:
    next_generation = set()
    for s in current_generation:
        candidates = reduce((lambda a, b: a & b), [connections[n] for n in s])
        for candidate in candidates:
            next_generation.add(s.union({candidate,}))
    if not next_generation:
        break
    current_generation = next_generation

max_clique = list(current_generation)[0]
print(','.join(sorted(max_clique)))
