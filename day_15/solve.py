grid = {}

robot_coords = None
dim = None

with open('input') as infile:
    map, commands = infile.read().split('\n\n')
    for x, line in enumerate(map.strip('\n').split('\n')):
        for y, char in enumerate(line.strip()):
            if char == '@':
                robot_coords = (x, y)
            elif char != '.':
                grid[(x, y)] = char
            dim = (x, y)

directions = {
    '^': (-1, 0),
    'v': (1, 0),
    '>': (0, 1),
    '<': (0, -1)
}

def can_move(c, d):
    nx, ny = (c[0]+d[0], c[1] + d[1])
    n = (nx, ny)
    if n not in grid:
        return True
    if grid[n] == '#':
        return False
    return can_move(n, d)

def do_move(c, d):
    n = (c[0]+d[0], c[1] + d[1])
    if n in grid:
       do_move(n, d)
    if grid.get(c) is not None:
        grid[n] = grid.pop(c)

for move in commands:
    if move not in directions:
        continue
    d = directions[move]
    if can_move(robot_coords, d):
        do_move(robot_coords, d)
        robot_coords = (robot_coords[0] + d[0], robot_coords[1] + d[1])

total = 0
for coord, item in grid.items():
    if item == 'O':
        x, y = coord
        total += 100*x + y

print(total)
