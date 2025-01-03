from dataclasses import dataclass
from dataclasses import field
from functools import cache
from pprint import pp
from copy import copy


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
    path: dict=field(default_factory=lambda: dict())
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

    def __hash__(self):
        return hash(self.coords)

    def __repr__(self):
        return self.symbol

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

    def unvisit(self):
        for direction in self.directions:
            self.visited[direction] = False
            self.distance[direction] = float('inf')


def should_replace(path, key, value):
    return key not in path or path[key] > value


def dijkstra(starting_node, starting_directions):
    nodes = []
    path = {}

    for direction in starting_directions:
        starting_node.distance[direction] = 0
        nodes.append((starting_node, direction, 0))
        path[(starting_node.coords, direction)] = 0

    while nodes:
        # Get node with smallest distance
        node, current_direction, current_cost = nodes.pop(0)

        if path[(node.coords, current_direction)] < current_cost:
            continue

        for cost, direction, neighbor in node.neighbors(current_direction):
            neighbor_cost = cost + node.distance[current_direction]
            neighbor.distance[direction] = min(neighbor.distance[direction], neighbor_cost)

            if direction != current_direction and should_replace(path, (node.coords, direction), current_cost + 1000):
                path[(node.coords, direction)] = current_cost + 1000

            if should_replace(path, (neighbor.coords, direction), neighbor_cost):
                path[(neighbor.coords, direction)] = neighbor_cost

            if not neighbor.visited[direction]:
                nodes.append((neighbor, direction, neighbor_cost))

        # mark current node as visited in current direction
        node.visited[current_direction] = True

        nodes.sort(key=lambda entry: min(entry[0].distance.values()))
    
    return path


def unvisit(matrix):
    for _, node in enumerate_n(matrix, n=2):
        node.unvisit()


def find_path(reindeer, target, matrix):
    from_reindeer = dijkstra(reindeer, ['east'])
    min_path_cost = min(target.distance.values())

    unvisit(matrix)

    from_target = dijkstra(target, [direction for direction in target.directions])

    path = set()
    oposite_direction = {
        'north': 'south',
        'south': 'north',
        'east': 'west',
        'west': 'east'
    }

    for coords, node in enumerate_n(matrix, n=2):
        for direction in target.directions:
            state_from_reindeer = (coords, direction)
            state_from_target = (coords, oposite_direction[direction])

            if state_from_reindeer in from_reindeer and state_from_target in from_target:
                if from_reindeer[state_from_reindeer] + from_target[state_from_target] == min_path_cost:
                    path.add(coords)

    return path


with open('input.txt') as f:
    lines = f.readlines()
    matrix = [list(l.strip()) for l in lines]

for coords, symbol in enumerate_n(matrix, n=2):
    matrix[coords[0]][coords[1]] = Node(symbol=symbol, coords=coords, matrix=matrix)

reindeer = next(node for _, node in enumerate_n(matrix, n=2) if node.symbol == 'S')
target = next(node for _, node in enumerate_n(matrix, n=2) if node.symbol == 'E')
path = find_path(reindeer, target, matrix)

print(len(path))
