from collections import Counter
import operator
import functools


with open('input') as infile:
    numbers = [int(line.strip()) for line in infile.read().strip().split('\n')]


def next_number(secret):
    secret = (secret ^ (secret * 64)) % 16777216
    secret = (secret ^ (secret // 32)) % 16777216
    secret = (secret ^ (secret * 2048)) % 16777216
    return secret

def advance(secret, amount):
    for _ in range(amount):
        secret = next_number(secret)
    return secret

print(sum(advance(secret, 2000) for secret in numbers))

def number_to_price_map(secret):
    prices = []
    generate = 2000
    for _ in range(generate):
        prices.append(secret % 10)
        secret = next_number(secret)
    differences = [None]
    for i in range(generate - 1):
        differences.append(prices[i+1] - prices[i])
    sequence_map = {}
    for i in range(4, generate):
        changes = tuple(differences[i-3:i+1])
        if changes not in sequence_map:
            sequence_map[changes] = prices[i]
    return Counter(sequence_map)

sequence_maps = [number_to_price_map(secret) for secret in numbers]
summed = functools.reduce(operator.add, sequence_maps)
print(summed.most_common(1)[0][1])
