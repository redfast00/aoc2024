import re
from collections import Counter

robots = []

GRID = (101, 103)
# GRID = (11, 7)

with open('input') as infile:
    for line in infile:
        rx, ry, dx, dy = [int(match[1]) for match in re.finditer(r'(-?\d+)', line)]
        robots.append(((rx, ry), (dx, dy)))

# part 1

simulation_time = 100
quadrants = Counter()

for ((rx, ry), (dx, dy)) in robots:
    nx = (rx + simulation_time*dx) % GRID[0]
    ny = (ry + simulation_time*dy) % GRID[1]
    if nx == GRID[0] // 2:
        continue
    if ny == GRID[1] // 2:
        continue
    
    qx = nx < GRID[0] // 2
    qy = ny < GRID[1] // 2
    quadrants[(qx, qy)] += 1

total = 1
for q, v in quadrants.items():
    total *= v

print(total)

# part 2

def display(robots, simulation_time):
    coords = set()
    for ((rx, ry), (dx, dy)) in robots:
        nx = (rx + simulation_time*dx) % GRID[0]
        ny = (ry + simulation_time*dy) % GRID[1]
        coords.add((nx, ny))
    for y in range(GRID[1]):
        sequential = 0
        sequential_max = 0
        for x in range(GRID[0]):
            if (x, y) in coords:
                sequential += 1
                sequential_max = max(sequential_max, sequential)
            else:
                sequential = 0
        if sequential_max > 10:
            return True
    return False


def actualdisplay(robots, simulation_time):
    coords = set()
    for ((rx, ry), (dx, dy)) in robots:
        nx = (rx + simulation_time*dx) % GRID[0]
        ny = (ry + simulation_time*dy) % GRID[1]
        coords.add((nx, ny))
    for y in range(GRID[1]):
        for x in range(GRID[0]):
            print(' ' if (x, y) not in coords else '#', end='')
        print()
    print(simulation_time)
    print("==================")


for simulation_time in range(0, 100000):
    if display(robots, simulation_time):
        actualdisplay(robots, simulation_time)
        break