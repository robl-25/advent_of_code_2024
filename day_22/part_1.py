PRUNE_NUMBER=16_777_216


def secret_numbers(seed):
    while True:
        seed = ((seed << 6) ^ seed) % PRUNE_NUMBER
        seed = ((seed >> 5) ^ seed) % PRUNE_NUMBER
        seed = ((seed << 11) ^ seed) % PRUNE_NUMBER

        yield seed


def nth_secret_number(seed, n):
    generator = secret_numbers(seed)

    for _ in range(n - 1):
        next(generator)

    return next(generator)


with open('input.txt') as f:
    seeds = [int(l) for l in f.readlines()]

total = 0

for seed in seeds:
    total += nth_secret_number(seed, 2_000)

print(total)
