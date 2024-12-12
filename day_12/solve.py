grid: dict[tuple[int, int], str] = {}

with open('input') as infile:
    for x, line in enumerate(infile):
        for y, char in enumerate(line.strip()):
            grid[(x, y)] = char

directions = [
    (-1, 0), # up
    (0, 1), # right
    (1, 0), # down
    (0, -1) # left
]

regions: list[tuple[str, set[tuple[int,int]]]] = []
to_explore = set(grid.keys())
already_assigned = set()

# calculate regions
while to_explore:
    starter = to_explore.pop()
    region = set([starter])
    region_explore = set([starter])
    plant_type = grid[starter]
    while region_explore:
        x, y = region_explore.pop()
        for (dx, dy) in directions:
            new_coord = (x+dx, y+dy)
            if new_coord in grid and new_coord not in region and grid[new_coord] == plant_type:
                region.add(new_coord)
                region_explore.add(new_coord)
                to_explore.remove(new_coord)
    regions.append((plant_type, region))


def calc_perimeter(region):
    total = 0
    for (x, y) in region:
        for (dx, dy) in directions:
            new_coord = (x+dx, y+dy)
            if new_coord not in region:
                total += 1
    return total

def calc_sides(region):
    total = 0
    # set of (inside, outside) tuple pairs
    fences = set()

    # calculate total perimeter and all (inside, outside) tuples
    for (x, y) in region:
        for (dx, dy) in directions:
            new_coord = (x+dx, y+dy)
            if new_coord not in region:
                total += 1
                fences.add(((x, y), new_coord))

    # calculate cost savings by combining multiple fences into one
    explored_fences = set()
    for starter_fence in fences:
        if starter_fence in explored_fences:
            continue
        this_combined_fence = set([starter_fence])
        this_gen_explore = set([starter_fence])

        while this_gen_explore:
            fence = this_gen_explore.pop()
            inside, outside = fence
            i_x, i_y = inside
            o_x, o_y = outside
            fence_direction = (i_x - o_x, i_y - o_y)
            # orthogonal to inside, outside fence direcction
            dx, dy = directions[(directions.index(fence_direction) + 1) % len(directions)]
            for direction_multiplier in (1, -1):
                neighbour_inside = (i_x + dx*direction_multiplier, i_y + dy*direction_multiplier)
                neighbour_outside = (o_x + dx*direction_multiplier, o_y + dy*direction_multiplier)
                neighbour_fence = (neighbour_inside, neighbour_outside)
                if neighbour_fence in fences and neighbour_fence not in this_combined_fence:
                    this_combined_fence.add(neighbour_fence)
                    this_gen_explore.add(neighbour_fence)
        explored_fences |= this_combined_fence
        total -= len(this_combined_fence) - 1
    return total

first = 0
second = 0
for (plant_type, region) in regions:
    area = len(region)
    perimeter = calc_perimeter(region)
    sides = calc_sides(region)
    first += area * perimeter
    second += area * sides

print(first)
print(second)
    