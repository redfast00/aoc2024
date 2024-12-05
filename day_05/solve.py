from collections import defaultdict

with open('input') as infile:
    dependency_chain_desc, content_list = [part.strip().split('\n') for part in infile.read().split('\n\n')]

dependency_graph = defaultdict(set)
for line in dependency_chain_desc:
    before, after = [int(a) for a in line.split('|')]
    dependency_graph[after].add(before)

def get_sorted_nodes(nodes, dependency_graph):
    # we can have a little O(n^3), as a treat
    relevant_nodes = set(nodes)
    sorted_nodes = []

    # list so input stays in order if already correct
    # not guaranteed in the task that there is a single ordering
    # but my input does seem to have a single ordering for every line
    remaining = list(nodes)
    used_set = set()
    
    while remaining:
        for node in remaining:
            if not ((dependency_graph[node] - used_set) & relevant_nodes):
                used_set.add(node)
                remaining.remove(node)
                sorted_nodes.append(node)
                break
        else:
            # guess we'll panic?
            1/0
    return sorted_nodes

middle_sum_correct = 0
middle_sum_wrong = 0

for line in content_list:
    nodes = [int(a) for a in line.split(',')]
    sorted_nodes = get_sorted_nodes(nodes, dependency_graph)
    if nodes == sorted_nodes:
        middle_sum_correct += sorted_nodes[(len(nodes)-1)//2]
    else:
        middle_sum_wrong += sorted_nodes[(len(nodes)-1)//2]
print(middle_sum_correct)
print(middle_sum_wrong)
