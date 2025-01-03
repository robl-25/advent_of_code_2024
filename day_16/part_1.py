from dataclasses import dataclass
from dataclasses import field
from functools import cache


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


ABSOLUTE_MIN=float('inf')


@dataclass 
class Node:
    symbol: str
    coords: tuple
    matrix: list=field(repr=False)
    visited: dict=field(
        default_factory=lambda: {
            'north': False,
            'south': False,
            'east': False,
            'west': False
        }
    )
    distance: dict=field(
        default_factory=lambda: {
            'north': float('inf'),
            'south': float('inf'),
            'east': float('inf'),
            'west': float('inf')
        }
    )

    directions = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1)
    }

    turns = {
        'north': ['east', 'west'],
        'south': ['east', 'west'],
        'east': ['north', 'south'],
        'west': ['north', 'south']
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

    def neighbors(self, current_direction):
        neighbors_with_cost = []

        neighbor = self._neighbor(current_direction)
            
        if neighbor and neighbor.symbol != '#':
            neighbors_with_cost.append((1, current_direction, neighbor))
        
        for direction in self.turns[current_direction]:
            neighbor = self._neighbor(direction)
            
            if neighbor and neighbor.symbol != '#':
                neighbors_with_cost.append((1001, direction, neighbor))

        return neighbors_with_cost


def fucking_dijkstra(starting_node):
    starting_node.distance['east'] = 0

    nodes = [(starting_node, 'east')]

    while nodes:
        # Get node with smallest distance
        node, current_direction = nodes.pop(0)

        if node.symbol == 'E':
            break

        for cost, direction, neighbor in node.neighbors(current_direction):
            neighbor.distance[direction] = min(neighbor.distance[direction], cost + node.distance[current_direction])

            if not neighbor.visited[direction]:
                nodes.append((neighbor, direction))

        # mark current node as visited in current direction
        node.visited[current_direction] = True

        nodes.sort(key=lambda entry: min(entry[0].distance.values()))


with open('input.txt') as f:
    matrix = [list(l.strip()) for l in f.readlines()]

for coords, symbol in enumerate_n(matrix, n=2):
    matrix[coords[0]][coords[1]] = Node(symbol=symbol, coords=coords, matrix=matrix)

reindeer = next(node for _, node in enumerate_n(matrix, n=2) if node.symbol == 'S')
target = next(node for _, node in enumerate_n(matrix, n=2) if node.symbol == 'E')

fucking_dijkstra(reindeer)

print(min(target.distance.values()))
