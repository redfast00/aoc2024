import re
from collections import deque
import itertools

with open('input') as infile:
    initial, gates = infile.read().split('\n\n')
    initial = {name: (int(value.strip())) for name, value in (line.split(':') for line in initial.split('\n')) }
    gates = sorted([(tuple(sorted((m[0], m[2]))), m[1], m[3]) for m in re.findall(r'(\w+) (\w+) (\w+) -> (\w+)', gates)])


operators = {
    'XOR': lambda a, b: a ^ b,
    'AND': lambda a, b: a & b,
    'OR':  lambda a, b: a | b
}

def solve(initial, gates):
    values = initial.copy()
    working_gates = deque(gates)

    while working_gates:
        v = working_gates.popleft()
        if all((wire in values) for wire in v[0]):
            (first, second), operation, destination = v
            values[destination] = operators[operation](values[first], values[second])
        else:
            working_gates.append(v)

    only_z = sorted(key for key in values.keys() if key.startswith('z'))
    bits = [values[k] for k in only_z]
    return bits

print(sum(bit * 2**idx for idx, bit in enumerate(solve(initial, gates))))

# manually constructed this; not ideal
swaps = [
    ('z06', 'vwr'),
    ('z11', 'tqm'),
    ('z16', 'kfs'),
    ('hcm', 'gfv')
]

for (swap_a, swap_b) in swaps:
    new_gates = []
    for (first, second), operation, destination in gates:
        if destination == swap_a:
            destination = swap_b
        elif destination == swap_b:
            destination = swap_a
        new_gates.append(((first, second), operation, destination))
    gates = new_gates

# rename the gates
renaming_map = {}
for (first, second), operation, destination in gates:
    if first.startswith('x') and second.startswith('y') and operation == 'AND' and not destination.startswith('z'):
        idx = int(first[1:])
        renaming_map[destination] = f'_{first}_AND_{second}'
    if first.startswith('x') and second.startswith('y') and operation == 'XOR' and not destination.startswith('z'):
        idx = int(first[1:])
        renaming_map[destination] = f'_{first}_XOR_{second}'

new_gates = []
for (first, second), operation, destination in gates:
    first = renaming_map.get(first, first)
    second = renaming_map.get(second, second)
    destination = renaming_map.get(destination, destination)
    new_gates.append((tuple(sorted((first, second))), operation, destination))

renamed_gates = sorted(new_gates).copy()

# print([k for k, v in renaming_map.items() if v == '_x36_XOR_y36'])

for (first, second), operation, destination in renamed_gates:
    first = renaming_map.get(first, first)
    second = renaming_map.get(second, second)
    destination = renaming_map.get(destination, destination)
    print(f'{first} {operation.ljust(3)} {second} -> {destination}')

modified_values = {k: 0 for k in initial.keys()}
# passing all zeroes to the initial values will always result in an all zero output, since there is no gate that can give a 1 when only given zeroes
register_range = int(max(initial.keys())[1:]) + 1
print(len(gates))
for idx in range(register_range):
    m = modified_values.copy()
    m[f'x{idx:02d}'] = 1
    expected = [0 for _ in range(register_range+1)]
    expected[idx] = 1
    actual_x = solve(m, gates)
    x_correct = actual_x == expected
    m = modified_values.copy()
    m[f'y{idx:02d}'] = 1
    expected = [0 for _ in range(register_range+1)]
    expected[idx] = 1
    actual_y = solve(m, gates)
    y_correct = actual_y  == expected
    m[f'y{idx:02d}'] = 1
    m[f'x{idx:02d}'] = 1
    expected = [0 for _ in range(register_range+1)]
    expected[idx+1] = 1
    actual_carry = solve(m, gates)
    carry_correct = actual_carry == expected
    if not (x_correct and y_correct and carry_correct):
        print(idx, x_correct, y_correct, carry_correct)
        print(actual_x)
        print(actual_y)
        print(actual_carry)

print(','.join(sorted(itertools.chain.from_iterable(swaps))))