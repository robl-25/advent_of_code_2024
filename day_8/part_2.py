from dataclasses import dataclass
from dataclasses import field
from collections import defaultdict
from itertools import permutations


def in_range(coords, matrix):
    if coords[0] not in range(len(matrix)):
        return False

    if coords[1] not in range(len(matrix[0])):
        return False

    return True


@dataclass
class Node:
    symbol: str
    coords: tuple
    matrix: list=field(repr=False)
    is_antinode: bool=False


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
    antenna_map = [list(l.strip()) for l in f.readlines()]

antennas = defaultdict(list)

for coords, symbol in enumerate_n(antenna_map, n=2):
    node = Node(symbol=symbol, coords=coords, matrix=antenna_map)
    
    antenna_map[coords[0]][coords[1]] = node

    if node.symbol != '.':
        antennas[node.symbol].append(node)

for k, v in antennas.items():
    if len(v) < 2:
        continue

    for a, b in permutations(v, 2):
        coord_final = (
            (b.coords[0] - a.coords[0]) + b.coords[0],
            (b.coords[1] - a.coords[1]) + b.coords[1]
        )
        a.is_antinode = True
        b.is_antinode = True

        while in_range(coord_final, antenna_map):
            antenna_map[coord_final[0]][coord_final[1]].is_antinode = True

            coord_final = (
                (b.coords[0] - a.coords[0]) + coord_final[0],
                (b.coords[1] - a.coords[1]) + coord_final[1]
            )

print(sum(node.is_antinode for _, node in enumerate_n(antenna_map, n=2)))
