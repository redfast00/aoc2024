def chunker(it,size):
    rv = [] 
    for i,el in enumerate(it,1) :   
        rv.append(el)
        if i % size == 0 : 
            yield rv
            rv = []
    if rv : yield rv


with open('input') as infile:
    line = infile.read().strip()
if len(line) % 2 != 0:
    line += '0'
parsed_disk = []
compact_disk = []
for id_, (filesize, free_space) in enumerate(chunker(line, 2)):
    parsed_disk.extend([id_] * int(filesize))
    parsed_disk.extend([None] * int(free_space))
    compact_disk.append((True, int(filesize), id_))
    compact_disk.append((False, int(free_space), None))

# part 1

disk = list(parsed_disk)
search_start_idx = 0
for source_idx in reversed(range(len(disk))):
    if disk[source_idx] is not None:
        for destination_idx in range(search_start_idx, source_idx):
            search_start_idx = destination_idx
            if disk[destination_idx] is None:
                disk[destination_idx] = disk[source_idx]
                disk[source_idx] = None
                break
        else:
            break

result = sum(idx * id_ for idx, id_ in enumerate(disk) if id_ is not None)
print(result)

# part 2

ids = [id_ for (is_in_use, _, id_) in compact_disk if is_in_use]

source_idx = len(compact_disk) - 1


for id_ in reversed(ids):
    # find index of source
    for potential_source_idx in range(source_idx, -1, -1):
        if compact_disk[potential_source_idx][2] == id_:
            source_idx = potential_source_idx
            break

    (is_source_in_use, source_size, source_id) = compact_disk[source_idx]
    assert is_source_in_use and source_id == id_
    if is_source_in_use:
        # find first slot where this one fits
        for destination_idx in range(0, source_idx):
            (is_destination_in_use, destination_size, destination_id) = compact_disk[destination_idx]
            if is_destination_in_use:
                continue
            if destination_size == source_size:
                compact_disk[destination_idx] = compact_disk[source_idx]
                compact_disk[source_idx] = (False, source_size, None)
                break
            elif destination_size > source_size:
                item = compact_disk[source_idx]
                free_space_remaining = (False, destination_size - source_size, None)
                compact_disk[source_idx] = (False, source_size, None)
                compact_disk[destination_idx] = free_space_remaining
                compact_disk.insert(destination_idx, item)
                break

idx = 0
total = 0

for (is_in_use, size, id_) in compact_disk:
    for _ in range(size):
        if is_in_use:
            total += idx * id_
        idx += 1

print(total)