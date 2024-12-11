from dataclasses import dataclass
from dataclasses import field


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
    height: int
    coords: tuple
    matrix: list=field(repr=False)
    visited: bool=False

    directions = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1)
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

    def _neighbors(self):
        return [self._neighbor(direction) for direction in self.directions if self._neighbor(direction) is not None]

    def _unvisited_neighbors(self):
        return [neighbor for neighbor in self._neighbors() if not neighbor.visited and neighbor.height == self.height + 1]

    def visit(self):
        self.visited = True

        for neighbor in self._unvisited_neighbors():
            neighbor.visit()

    def reset(self):
        self.visited = False

        for neighbor in self._neighbors():
            if neighbor.visited:
                neighbor.reset()


with open('input.txt') as f:
    topographical_map = [list(line.strip()) for line in f.readlines()]

for coords, height in enumerate_n(topographical_map, n=2):
    node = Node(
        height=int(height),
        coords=coords,
        matrix=topographical_map
    )

    topographical_map[coords[0]][coords[1]] = node


trailheads = [node for _, node in enumerate_n(topographical_map, n=2) if node.height == 0]
total = 0

for trailhead in trailheads:
    trailhead.visit()
    
    total += sum(node.visited for _, node in enumerate_n(topographical_map, n=2) if node.height == 9)

    trailhead.reset()

print(total)
