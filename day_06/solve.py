with open('input') as infile:
    lines = infile.read().strip().split('\n')

obstacles = {}

start_position = None

for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char == '.':
            obstacles[(i, j)] = False
        elif char == '#':
            obstacles[(i, j)] = True
        elif char == '^':
            obstacles[(i, j)] = False
            start_position = (i, j)
        else:
            1/0


direction_order = [
    (-1, 0), # up
    (0, 1), # right
    (1, 0), # down
    (0, -1) # left
]

def solve_1():
    direction_idx = 0
    current_position = start_position
    visited_coordinates = set()

    while True:
        direction = direction_order[direction_idx]
        visited_coordinates.add(current_position)
        next_position = (current_position[0]+direction[0], current_position[1]+direction[1])
        if next_position not in obstacles:
            break
        if obstacles[next_position]:
            direction_idx = (direction_idx + 1) % len(direction_order)
            continue
        else:
            current_position = next_position
    print(len(visited_coordinates))
    return visited_coordinates

def does_extra_object_cause_loop(obstacle_coords):
    visited = set() # set of coordinate, direction
    direction_idx = 0
    current_position = start_position

    while True:
        direction = direction_order[direction_idx]
        if (current_position, direction) in visited:
            return True
        visited.add((current_position, direction))
        next_position = (current_position[0]+direction[0], current_position[1]+direction[1])
        if next_position not in obstacles:
            # escaped the map
            return False
        if obstacles[next_position] or next_position == obstacle_coords:
            direction_idx = (direction_idx + 1) % len(direction_order)
            continue
        else:
            current_position = next_position

def solve_2(visited):
    total = 0
    for (i, j) in visited:
        if (i, j) == start_position:
            continue
        if does_extra_object_cause_loop((i, j)):
            total += 1
    print(total)

visited = solve_1()
print(len(visited)/len(obstacles))
solve_2(visited)
