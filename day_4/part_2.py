from dataclasses import dataclass
from dataclasses import field
from collections import Counter

# Enumerate iterable containing iterables recursively.
#
# Like `enumerate` but can recursively go into nested iterables yielding each
# entry's index as a tuple.
#
#
# Sample usage:
#
#   >>> list(enumerate_n('123'))
#   [(0, '1'), (1, '2'), (2, '3')]
#
#   >>> list(enumerate_n(['123']))
#   [(0, '123')]
#
#   >>> list(enumerate_n(['123'], n=2))
#   [((0, 0), '1'), ((0, 1), '2'), ((0, 2), '3')]
#
#   >>> list(enumerate_n(['123', [1, 2]], n=2))
#   [((0, 0), '1'),
#    ((0, 1), '2'),
#    ((0, 2), '3'),
#    ((1, 0), 1),
#    ((1, 1), 2)]
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


@dataclass 
class Node:
    symbol: str
    coords: tuple
    matrix: list=field(repr=False)

    directions = {
        'northeast': (-1, 1),
        'northwest': (-1, -1),
        'southeast': (1, 1),
        'southwest': (1, -1)
    }

    def _neighbor(self, direction):
        neighbor_coords = (
            self.coords[0] + self.directions[direction][0],
            self.coords[1] + self.directions[direction][1]
        )

        if neighbor_coords[0] not in range(len(self.matrix)):
            return None

        if neighbor_coords[1] not in range(len(self.matrix[0])):
            return None

        return self.matrix[neighbor_coords[0]][neighbor_coords[1]]

    def neighbors(self):
        return [self._neighbor(direction) for direction in self.directions if self._neighbor(direction) is not None]

    def is_xmas(self):
        valid_neighbors = [
            ['S', 'S', 'M', 'M'],
            ['M', 'M', 'S', 'S'],
            ['S', 'M', 'S', 'M'],
            ['M', 'S', 'M', 'S']
        ]

        return self.symbol == 'A' and [neighbor.symbol for neighbor in self.neighbors()] in valid_neighbors


with open('input.txt') as f:
    word_search = [list(l.strip()) for l in f.readlines()]

for coords, symbol in enumerate_n(word_search, n=2):
    word_search[coords[0]][coords[1]] = Node(symbol=symbol, coords=coords, matrix=word_search)

print(len([node for _, node in enumerate_n(word_search, n=2) if node.is_xmas()]))
