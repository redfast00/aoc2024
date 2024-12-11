from collections import Counter

with open('input') as infile:
    input_stones = Counter(stone for stone in infile.read().strip().split())

def blink(stones):
    result = Counter()
    for stone, amount in stones.items():
        if stone == '0':
            result['1'] += amount
        elif len(stone) % 2 == 0:
            result[stone[:len(stone)//2]] += amount
            result[str(int(stone[len(stone)//2:]))] += amount
        else:
            result[str(int(stone)*2024)] += amount
    return result

stones = input_stones

for idx in range(75):
    stones = blink(stones)
    if idx + 1 == 25:
        print(stones.total())
print(stones.total())
