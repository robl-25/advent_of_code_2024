from dataclasses import dataclass
from dataclasses import field
from collections import Counter
from itertools import product
from pprint import pp
import heapq

MAX_CHEAT_SIZE=2


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
    distance: int=float('inf')

    directions = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1)
    }
    
    # Gets neighbor in `self.matrix` given a `direction`.
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

    # All neighbors in `self.directions`.
    def neighbors(self):
        return [self._neighbor(direction) for direction in self.directions if self._neighbor(direction) is not None]

    def manhattan_distance(self, other):
        return abs(self.coords[0] - other.coords[0]) + abs(self.coords[1] - other.coords[1])

    # Makes nodes equal if they have the same `coords`.
    def __eq__(self, other):
        return self.coords == other.coords

    def __lt__(self, other):
        return self.distance < other.distance

    def __hash__(self):
        return hash(self.coords)

    def unvisit(self):
        self.visited = False


def unvisit(matrix):
    for _, node in enumerate_n(matrix, n=2):
        node.unvisit()


# Finds distance from given `node` to every other node in the graph.optionally
# stopping at `target_symbol`.
def dijkstra(node, target_symbol=None):
    node.distance = 0

    nodes = [node]
    heapq.heapify(nodes)

    while nodes:
        # Get node with smallest distance
        node = heapq.heappop(nodes)

        if node.visited:
            continue

        # Mark current node as visited in current direction
        node.visited = True

        # Optionally stop search when we reach the given `target_symbol`
        if target_symbol and node.symbol == target_symbol:
            break

        for neighbor in node.neighbors():
            neighbor.distance = min(neighbor.distance, node.distance + 1)

            if not neighbor.visited and neighbor.symbol != '#':
                heapq.heappush(nodes, neighbor)


with open('input.txt') as f:
    matrix = [list(l.strip()) for l in f.readlines()]

for coords, symbol in enumerate_n(matrix, n=2):
    matrix[coords[0]][coords[1]] = Node(symbol=symbol, coords=coords, matrix=matrix)

start = next(node for _, node in enumerate_n(matrix, n=2) if node.symbol == 'S')
end = next(node for _, node in enumerate_n(matrix, n=2) if node.symbol == 'E')

dijkstra(end)
unvisit(matrix)

reachable_nodes = [node for _, node in enumerate_n(matrix, n=2) if node.symbol != '#' and node.distance < float('inf')]
cheat_nodes = set()

for a, b in product(reachable_nodes, reachable_nodes):
    if a.manhattan_distance(b) in range(2, MAX_CHEAT_SIZE + 1) and (b, a) not in cheat_nodes:
        cheat_nodes.add((a, b))


counter = Counter(abs(a.distance - b.distance) - a.manhattan_distance(b) for a, b in cheat_nodes)

print(sum(value for key, value in counter.items() if key >= 100 and key < float('inf')))
