import functools


with open('input') as infile:
    towels, designs = infile.read().split('\n\n')
    towels = tuple(towel.strip() for towel in towels.strip().split(','))
    designs = designs.strip().split('\n')

@functools.cache
def num_designs(design, towels):
    counter = 0
    for towel in towels:
        if design.startswith(towel):
            if design == towel:
                counter += 1
            else:
                counter += num_designs(design[len(towel):], towels)
    return counter

first = 0
second = 0
for design in designs:
    num = num_designs(design, towels)
    first += (num != 0)
    second += num
print(first)
print(second)
