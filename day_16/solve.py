import heapq

start_coords = None
finish_coords = None


walls = {}
with open('input') as infile:
    for x, line in enumerate(infile):
        for y, char in enumerate(line.strip()):
            if char == 'S':
                start_coords = (x, y)
            elif char == 'E':
                finish_coords = (x, y)
            elif char == '#':
                walls[(x, y)] = True

directions = [
    (-1, 0), # up
    (0, 1), # right
    (1, 0), # down
    (0, -1) # left
]

# score, direction_idx, coords, history
work_q = []

heapq.heappush(work_q, (0, 1, start_coords, [start_coords]))

explored = dict()

finish_score = None

while True:
    (score, direction_idx, (x, y), history) = heapq.heappop(work_q)
    cache_key = ((x, y), direction_idx)
    if cache_key in explored and explored[cache_key] < score:
        continue
    explored[cache_key] = score
    if (x, y) == finish_coords:
        # push back on the heap for later processing
        heapq.heappush(work_q, (score, direction_idx, (x, y), history))
        finish_score = score
        break
    heapq.heappush(work_q, (score + 1000, (direction_idx + 1) % 4, (x, y), history))
    heapq.heappush(work_q, (score + 1000, (direction_idx - 1) % 4, (x, y), history))
    (dx, dy) = directions[direction_idx]
    new_coords = (x+dx, y+dy)
    if new_coords not in walls:
        heapq.heappush(work_q, (score + 1, direction_idx, new_coords, history + [new_coords]))

print(finish_score)

visited_set = set()
visited_set.add(finish_coords)

while True:
    (score, direction_idx, (x, y), history) = heapq.heappop(work_q)
    if score != finish_score:
        break
    if (x, y) == finish_coords:
        for tile in history:
            visited_set.add(tile)
print(len(visited_set))
