import heapq
import itertools
import collections

allowed = {}

startpos = None
endpos = None

with open('input') as infile:
    for x, line in enumerate(infile):
        for y, char in enumerate(line.strip()):
            if char == 'S':
                startpos = (x, y)
            elif char == 'E':
                endpos = (x, y)
            if char != '#':
                allowed[(x, y)] = True

directions = [
    (-1, 0), # up
    (0, 1), # right
    (1, 0), # down
    (0, -1) # left
]

def solve():
    to_explore = []
    explored = {}

    heapq.heappush(to_explore, (0, startpos, [startpos]))


    while to_explore:
        cost, coord, path = heapq.heappop(to_explore)
        if coord in explored and explored[coord] < cost:
            continue
        explored[coord] = cost
        if coord == endpos:
            return path + [coord]
        for direction in directions:
            new_coord = (coord[0]+direction[0], coord[1]+direction[1])
            if allowed.get(new_coord):
                heapq.heappush(to_explore, (cost + 1, new_coord, path + [new_coord]))

path = solve()

progress = {coord: idx for idx, coord in enumerate(path)}


def generate_offset_circle(radius):
    offsets = set()
    radius = radius + 1
    for horizontal_amount in range(radius):
        for vertical_amount in range(radius - horizontal_amount):
            for hmul in (-1, 1):
                for vmul in (-1, 1):
                    offsets.add((horizontal_amount*hmul, vertical_amount*vmul))
    return offsets

def distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)

offset = generate_offset_circle(20)

saving = collections.Counter()


for coord in path:
    progress_before_cheat = progress[coord]
    for (dx, dy) in offset:
        x, y = coord
        new_coord = (x+dx, y+dy)
        if new_coord in progress and (saved := (progress[new_coord] - (progress_before_cheat + distance(coord, new_coord)))) > 0:
            if new_coord == endpos:
                saved -= 1
            saving[saved] += 1

# for saved in sorted(saving.keys()):
#     print(f'There are {saving[saved]} cheats that save {saved} picoseconds')

total = 0
for (saved, amount) in saving.items():
    if saved >= 100:
        total += amount
print(total)


