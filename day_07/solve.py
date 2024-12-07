def recurse(desired, remaining_values, stack, enable_extra_operator=False):
    if not remaining_values:
        return stack == desired
    if stack > desired:
        return False
    if recurse(desired, remaining_values[1:], stack + remaining_values[0], enable_extra_operator=enable_extra_operator):
        return True
    if recurse(desired, remaining_values[1:], stack * remaining_values[0], enable_extra_operator=enable_extra_operator):
        return True
    if enable_extra_operator and recurse(desired, remaining_values[1:], int(str(stack) +  str(remaining_values[0])), enable_extra_operator=enable_extra_operator):
        return True

def is_possible(desired, values, enable_extra_operator=False):
    if len(values) == 1:
        return values[0] == desired
    return recurse(desired, values[1:], values[0], enable_extra_operator=enable_extra_operator)


first = 0
second = 0

with open('input') as infile:
    for line in infile:
        desired, values = line.split(':')
        desired = int(desired)
        values = [int(v) for v in values.strip().split(' ')]
        if is_possible(desired, values):
            first += desired
        if is_possible(desired, values, enable_extra_operator=True):
            second += desired

print(first)
print(second)
