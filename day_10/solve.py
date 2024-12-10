grid = {}

with open('input') as infile:
    for x, line in enumerate(infile):
        for y, char in enumerate(line.strip()):
            value = int(char) if char.isnumeric() else None
            grid[(x, y)] = value

directions = [
    (-1, 0), # up
    (0, 1), # right
    (1, 0), # down
    (0, -1) # left
]

def get_tops_of_trailhead(grid, coords, level):
    x, y = coords
    retval = set()
    for (dx, dy) in directions:
        new = (x+dx, y+dy)
        if grid.get(new) == level:
            if level == 9:
                retval.add(new)
            else:
                retval |= get_tops_of_trailhead(grid, new, level + 1)
    return retval

def get_path_to_top(grid, coords, level):
    x, y = coords
    retval = set()
    for (dx, dy) in directions:
        new = (x+dx, y+dy)
        if grid.get(new) == level:
            if level == 9:
                retval.add((new,))
            else:
                paths_from_here = get_path_to_top(grid, new, level + 1)
                retval |= set((new,) + path for path in paths_from_here)
    return retval

solution_1 = 0
solution_2 = 0
for coord, value in grid.items():
    if value == 0:
        score = len(get_tops_of_trailhead(grid, coord, 1))
        solution_1 += score
        rating = len(get_path_to_top(grid, coord, 1))
        solution_2 += rating

print(solution_1)
print(solution_2)