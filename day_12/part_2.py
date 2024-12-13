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
class Region:
    plots: set=field(default_factory=set)

    def _check_corners(self, neighbors, vertical_direction, horizontal_direction):
        if neighbors[vertical_direction] not in self.plots and neighbors[horizontal_direction] not in self.plots:
            return 1
        
        if neighbors[vertical_direction] in self.plots and neighbors[horizontal_direction] in self.plots:
            return neighbors[vertical_direction + horizontal_direction] not in self.plots

        return 0


    def corners(self):
        corners_total = 0
        
        for plot in self.plots:
            neighbors =  {
                'north': plot._neighbor('north'),
                'south': plot._neighbor('south'),
                'west': plot._neighbor('west'),
                'east': plot._neighbor('east'),
                'northeast': plot._extra_neighbor('northeast'),
                'northwest': plot._extra_neighbor('northwest'),
                'southeast': plot._extra_neighbor('southeast'),
                'southwest': plot._extra_neighbor('southwest')
            }

            corners_total += self._check_corners(neighbors, 'north', 'west')
            corners_total += self._check_corners(neighbors, 'north', 'east')
            corners_total += self._check_corners(neighbors, 'south', 'west')
            corners_total += self._check_corners(neighbors, 'south', 'east')

        return corners_total


    def perimeter(self):
        return sum(plot.fenceable_neighbors() for plot in self.plots)

    def area(self):
        return len(self.plots)


@dataclass 
class Node:
    symbol: str
    coords: tuple
    matrix: list=field(repr=False)
    visited: bool=False

    directions = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1)
    }

    extra_directions = {
        'northeast': (-1, 1),
        'northwest': (-1, -1),
        'southeast': (1, 1),
        'southwest': (1, -1)
    }

    def __hash__(self):
        return id(self)

    def _extra_neighbor(self, direction):
        neighbor_coords = (
            self.coords[0] + self.extra_directions[direction][0],
            self.coords[1] + self.extra_directions[direction][1]
        )

        if neighbor_coords[0] not in range(len(self.matrix)):
            return None

        if neighbor_coords[1] not in range(len(self.matrix[0])):
            return None

        return self.matrix[neighbor_coords[0]][neighbor_coords[1]]

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
        return [self._neighbor(direction) for direction in self.directions]

    def fenceable_neighbors(self):
        return sum(1 for neighbor in self.neighbors() if neighbor is None or neighbor.symbol != self.symbol)

    def visit(self):
        self.visited = True


def build_region(plot):
    region = Region()

    plots = [plot]
    visited_plots = {plot}

    for plot in plots:
        plot.visit()
        region.plots.add(plot)

        for neighbor in plot.neighbors():
            if neighbor is not None and not neighbor.visited and neighbor.symbol == plot.symbol and neighbor not in visited_plots:
                plots.append(neighbor)
                visited_plots.add(neighbor)

    return region


with open('input.txt') as f:
    plots = [list(l.strip()) for l in f.readlines()]

for coords, symbol in enumerate_n(plots, n=2):
    plots[coords[0]][coords[1]] = Node(symbol=symbol, coords=coords, matrix=plots)

regions = []

for coords, plot in enumerate_n(plots, n=2):
    if not plot.visited:
        regions.append(build_region(plot))

total = 0

for region in regions:
    total += region.corners() * region.area()

print(total)
