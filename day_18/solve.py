import heapq
import bisect

obstacles = []

with open('input') as infile:
    for line in infile:
        obstacles.append(tuple(int(p) for p in line.strip().split(',')))

GRID_DIMS = (71, 71) # 0 to 70, inclusive
FINISH_COORDS = (70, 70)

directions = [
    (-1, 0), # up
    (0, 1), # right
    (1, 0), # down
    (0, -1) # left
]

def solve(cutoff):
    grid = {}
    for obstacle in obstacles[:cutoff]:
        grid[obstacle] = True

    to_explore = []
    explored = {}

    heapq.heappush(to_explore, (0, (0, 0)))

    finish_score = None

    while to_explore:
        cost, coord = heapq.heappop(to_explore)
        if coord in explored and explored[coord] <= cost:
            continue
        explored[coord] = cost
        if coord == FINISH_COORDS:
            finish_score = cost
            break
        for direction in directions:
            new_coord = (coord[0]+direction[0], coord[1]+direction[1])
            if new_coord[0] in range(GRID_DIMS[0]) and new_coord[1] in range(GRID_DIMS[1]) and new_coord not in grid:
                heapq.heappush(to_explore, (cost + 1, new_coord))
    return finish_score

print(solve(1024))

# binary search first cutoff that doesn't work anymore
# key will transform the list of indices into a virtual list of [False, False, False, ..., False, True, True, True, ...]
# bisect left will return the index of the first True key

cutoff = bisect.bisect_left(
    list(range(len(obstacles))),
    True,
    lo=1024,
    key=lambda i: solve(i) is None
)
print(','.join(str(c) for c in obstacles[cutoff - 1]))
