from dataclasses import dataclass
from dataclasses import field
from itertools import batched
import re
from pprint import pp
from functools import cache


@dataclass 
class Button:
    step: tuple
    cost: int

    def __hash__(self):
        return id(self)


@dataclass
class Prize:
    coords: tuple

    def __hash__(self):
        return id(self)


@dataclass
class Machine:
    button_a: Button
    button_b: Button
    prize: Prize


@cache
def tokens(button_a, button_b, prize, current_cost, current_position, button_presses):
    if current_position == prize.coords:
        return current_cost

    if current_position[0] > prize.coords[0]:
        return float('inf')

    if current_position[1] > prize.coords[1]:
        return float('inf')

    if button_presses[0] >= 100 or button_presses[1] >= 100:
        return float('inf')

    coords_a = (
        current_position[0] + button_a.step[0],
        current_position[1] + button_a.step[1]
    )

    result_a = tokens(
        button_a,
        button_b,
        prize,
        current_cost + button_a.cost,
        coords_a,
        (
            button_presses[0] + 1,
            button_presses[1]
        )
    )

    coords_b = (
        current_position[0] + button_b.step[0],
        current_position[1] + button_b.step[1]
    )

    result_b = tokens(
        button_a,
        button_b,
        prize,
        current_cost + button_b.cost,
        coords_b,
        (
            button_presses[0],
            button_presses[1] + 1
        )
    )

    return min(result_a, result_b)


with open('input.txt') as f:
    lines = [l.strip() for l in f.readlines() if l != '\n']

machines = []

button_regex = re.compile(r"X\+(\d+), Y\+(\d+)")
prize_regex = re.compile(r"X=(\d+), Y=(\d+)")

for a, b, prize in batched(lines, n=3):
    [(x, y)] = button_regex.findall(a) 

    button_a = Button(
        step=(int(x), int(y)),
        cost=3
    )

    [(x, y)] = button_regex.findall(b)

    button_b = Button(
        step=(int(x), int(y)),
        cost=1
    )

    [(x, y)] = prize_regex.findall(prize)

    prize = Prize(coords=(int(x), int(y)))

    machine = Machine(
        button_a=button_a,
        button_b=button_b,
        prize=prize
    )

    machines.append(machine)

total_cost = 0

for machine in machines:
    cost = tokens(
        machine.button_a,
        machine.button_b,
        machine.prize,
        0,
        (0, 0),
        (0, 0)
    )

    if cost < float('inf'):
        total_cost += cost

print(total_cost)
