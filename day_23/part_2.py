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

cliques = [{node} for node in nodes.values()]

for node in nodes.values():
    for clique in cliques:
        if all(node in n.neighbors for n in clique):
            clique.add(node)

max_clique = sorted(i.symbol for i in max(cliques, key=len))
print(','.join(max_clique))