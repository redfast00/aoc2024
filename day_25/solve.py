import itertools

def parse_key(text):
    depth_map = {}
    for idx, line in enumerate(text.strip().split('\n')):
        for jdx, char in enumerate(line):
            if char == '#' and jdx not in depth_map:
                depth_map[jdx] = 6 - idx
    return [v for _, v in sorted(depth_map.items())]

def parse_lock(text):
    depth_map = {}
    for idx, line in enumerate(text.strip().split('\n')):
        for jdx, char in enumerate(line):
            if char == '.' and jdx not in depth_map:
                depth_map[jdx] = idx - 1
    return [v for _, v in sorted(depth_map.items())]

locks = []
keys = []

with open('input') as infile:
    for item in infile.read().split('\n\n'):
        if item[0] == '.':
            keys.append(parse_key(item))
        else:
            locks.append(parse_lock(item))

total = 0
for key, lock in itertools.product(keys, locks):
    for key_pin, lock_pin in zip(key, lock):
        if key_pin + lock_pin >= 6:
            break
    else:
        total += 1
print(total)