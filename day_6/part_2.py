from dataclasses import dataclass
from dataclasses import field

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
    visited: bool=False
    visited_directions: set=field(default_factory=set)

    directions = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1)
    }

    def neighbor(self, direction):
        neighbor_coords = (
            self.coords[0] + self.directions[direction][0],
            self.coords[1] + self.directions[direction][1]
        )

        if neighbor_coords[0] not in range(len(self.matrix)):
            return None

        if neighbor_coords[1] not in range(len(self.matrix[0])):
            return None

        return self.matrix[neighbor_coords[0]][neighbor_coords[1]]

    def reset(self):
        self.visited = False
        self.visited_directions = set()


def is_cycle(lab_map, direction, guard):
    while True:
        guard.visited = True
        guard.visited_directions.add(direction)

        neighbor = guard.neighbor(direction)

        if neighbor is None:
            return False

        if neighbor.visited and direction in neighbor.visited_directions:
            return True

        if neighbor.symbol == '#':
            direction = turn_right[direction]
            continue
        
        guard = neighbor


with open('input.txt') as f:
    lab_map = [list(l.strip()) for l in f.readlines()]

for coords, symbol in enumerate_n(lab_map, n=2):
    lab_map[coords[0]][coords[1]] = Node(symbol=symbol, coords=coords, matrix=lab_map)

directions = {
    '^': 'north',
    '<': 'west',
    '>': 'east',
    'v': 'south'
}


turn_right = {
    'north': 'east',
    'south': 'west',
    'west': 'north',
    'east': 'south'
}

guard = next(node for _, node in enumerate_n(lab_map, n=2) if node.symbol in {'^', '<', '>', 'v'})
direction = directions[guard.symbol]

initial_coords = guard.coords

guard.symbol = '.'

eligible_obstacles = [node for _, node in enumerate_n(lab_map, n=2) if node.symbol == '.']
total = 0

print(f'Total: {len(eligible_obstacles)}')

for index, eligible_obstacle in enumerate(eligible_obstacles):
    print(f'{index}/{len(eligible_obstacles)} - {((index + 1) * 100) / len(eligible_obstacles):.3f}%', end='\r')
    eligible_obstacle.symbol = '#'

    if is_cycle(lab_map, direction, guard):
        total += 1

    eligible_obstacle.symbol = '.'

    # Reset map
    for _, node in enumerate_n(lab_map, n=2):
        node.reset()

print()
print(total)
