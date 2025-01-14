from collections import defaultdict

PRUNE_NUMBER=16_777_216


def sliding_window(iterable, n=2):
    from itertools import islice

    args = [islice(iterable, i, None) for i in range(n)]
    return zip(*args)


def prices(seed):
    n = 0

    for n in range(2_001):
        yield seed % 10

        seed = ((seed << 6) ^ seed) % PRUNE_NUMBER
        seed = ((seed >> 5) ^ seed) % PRUNE_NUMBER
        seed = ((seed << 11) ^ seed) % PRUNE_NUMBER


with open('input.txt') as f:
    seeds = [int(l) for l in f.readlines()]

scores = defaultdict(int)

for seed in seeds:
    daily_prices = list(prices(seed))
    unique_variations = set()

    last = daily_prices[0]

    for a, b, c, d in sliding_window(daily_prices, n=4):
        variations = (
            a - last,
            b - a,
            c - b,
            d - c
        )

        if variations not in unique_variations:
            scores[variations] += d
            unique_variations.add(variations)

        last = a

max_sequence, max_value = max(scores.items(), key=lambda item: item[1])

print(max_value)
