from dataclasses import dataclass


@dataclass
class Rule:
    upper: int
    lower: int

    def applicable(self, printing_order_set):
        return self.upper in printing_order_set and self.lower in printing_order_set

    def is_followed(self, printing_order):
        upper_index = printing_order.index(self.upper)
        lower_index = printing_order.index(self.lower)

        return upper_index > lower_index


def is_valid(printing_order):
    printing_order_set = set(printing_order)

    for rule in rules:
        if rule.applicable(printing_order_set) and not rule.is_followed(printing_order):
            return False
        
    return True


with open('input.txt') as f:
    lines = f.readlines()

splitting_index = lines.index('\n')

rules_input = lines[:splitting_index]
data_input = lines[splitting_index + 1:]

rules = []

for line in rules_input:
    lower, upper = line.strip().split('|')
    rules.append(Rule(upper=int(upper), lower=int(lower)))

data = []

for line in data_input:
    data.append([int(i) for i in line.strip().split(',')])

total = 0

for printing_order in data:
    if is_valid(printing_order):
        total += printing_order[len(printing_order) // 2]

print(total)
