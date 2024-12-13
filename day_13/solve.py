import re
import numpy as np

with open('input') as infile:
    content = infile.read()

def tokens_to_solve(a, b, prize_coords):
    minimal_tokens_possible = float('inf')
    for a_presses in range(100):
        a_reach = (a_presses*a[0], a_presses*a[1])
        difference_x = prize_coords[0] - a_reach[0]
        if difference_x < 0:
            continue
        if difference_x % b[0] != 0:
            continue
        b_presses = difference_x // b[0]
        if a_reach[1] + b_presses*b[1] != prize_coords[1]:
            continue
        cost = 3*a_presses + b_presses
        if cost < minimal_tokens_possible:
            minimal_tokens_possible = cost
    return minimal_tokens_possible if minimal_tokens_possible != float('inf') else None

def tokens_to_solve_2(a, b, prize_coords):
    # Apparently a * x = b or b * x = a does not happen in the input :)
    challenge = np.array([[a[0], b[0]], [a[1], b[1]]])
    solution = np.array([prize_coords[0], prize_coords[1]])
    x = np.linalg.solve(challenge, solution)
    a_presses = round(x[0])
    b_presses = round(x[1])

    if a_presses*a[0] + b_presses*b[0] != prize_coords[0]:
        return None
    if a_presses*a[1] + b_presses*b[1] != prize_coords[1]:
        return None

    if a_presses < 0 or b_presses < 0:
        return None

    cost = 3*a_presses + b_presses
    return cost

first = 0
second = 0

for problem in content.split('\n\n'):
    button_a, button_b, prize = problem.strip().split('\n')
    a = [int(m[1]) for m in re.finditer(r'(\d+)', button_a)]
    b = [int(m[1]) for m in re.finditer(r'(\d+)', button_b)]
    prize_coords = [int(m[1]) for m in re.finditer(r'(\d+)', prize)]
    cost = tokens_to_solve(a, b, prize_coords)
    first += cost if cost is not None else 0

    prize_coords[0] += 10000000000000
    prize_coords[1] += 10000000000000
    cost = tokens_to_solve_2(a, b, prize_coords)
    second += cost if cost is not None else 0


print(first)
print(second)
