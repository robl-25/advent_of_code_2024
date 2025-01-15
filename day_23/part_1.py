from dataclasses import dataclass
from dataclasses import field
from pprint import pp


@dataclass
class Node:
    symbol: str
    neighbors: set=field(repr=False, default_factory=set)

    def __hash__(self):
        return hash(self.symbol)

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)


with open('input.txt') as f:
    data = [line.strip().split('-') for line in f.readlines()]

nodes = {}

for node_a, node_b in data:
    if node_a not in nodes:
        nodes[node_a] = Node(symbol=node_a)

    if node_b not in nodes:
        nodes[node_b] = Node(symbol=node_b)

    node_a = nodes[node_a]
    node_b = nodes[node_b]

    node_a.add_neighbor(node_b)
    node_b.add_neighbor(node_a)

cycles = set()

nodes_t = (n for n in nodes.values() if n.symbol.startswith('t'))

for node in nodes_t:
    for neighbor in node.neighbors:
        overlap = node.neighbors & neighbor.neighbors

        if overlap:
            for entry in overlap:
                entries = [entry.symbol, node.symbol, neighbor.symbol]
                entries.sort()
                cycles.add(tuple(entries))

total = 0

for cycle in cycles:
    if len(cycle) == 3:
        total += 1

print(total)
