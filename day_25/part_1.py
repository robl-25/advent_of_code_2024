from collections import Counter
from itertools import product


def is_lock(matrix):
    return all(item == '#' for item in matrix[0])


def compute_heights(matrix):
    c = Counter(coords[1] for coords, symbol in enumerate_n(matrix, n=2) if symbol == '#')

    result = [0] * len(matrix[0])

    for col, count in c.items():
        result[col] = count

    return result

def enumerate_n(iterable, start=0, n=1):
    from collections.abc import Iterable

    count = start

    for item in iterable:
        if isinstance(item, Iterable) and n > 1:
            for index, value in enumerate_n(iter(item), start=start, n=n - 1):
                if not isinstance(index, Iterable):
                    index = [index]

                yield tuple([count, *index]), value
        else:
            yield count, item

        count += 1


with open('input.txt') as f:
    schematics = f.read().split('\n\n')

keys = []
locks = []

for schematic in schematics:
    matrix = [list(l.strip()) for l in schematic.splitlines()]

    if is_lock(matrix):
        matrix = matrix[1:]
        heights = compute_heights(matrix)

        keys.append(heights)
    else:
        matrix = matrix[:-1]
        heights = compute_heights(matrix)

        locks.append(heights)

total = 0

for key, lock in product(keys, locks):
    if all(k + l <= 5 for k, l in zip(key, lock)):
        total += 1

print(total)
