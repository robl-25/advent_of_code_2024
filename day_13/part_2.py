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
def tokens(button_a, button_b, prize, current_cost, current_position):
    if current_position == prize.coords:
        return current_cost

    if current_position[0] > prize.coords[0]:
        return float('inf')

    if current_position[1] > prize.coords[1]:
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
        coords_a
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
        coords_b
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

    prize = Prize(coords=(int(x) + 10_000_000_000_000, int(y) + 10_000_000_000_000))

    machine = Machine(
        button_a=button_a,
        button_b=button_b,
        prize=prize
    )

    machines.append(machine)

total_cost = 0

for machine in machines:
    x_a, y_a = machine.button_a.step
    x_b, y_b = machine.button_b.step
    x_t, y_t = machine.prize.coords

    a = (y_t - (y_b * x_t / x_b)) / (y_a - (x_a * y_b / x_b))
    b = (x_t - (x_a * a)) / x_b

    a = round(a)
    b = round(b)

    if (a * x_a + b * x_b != x_t) or (a * y_a + b * y_b != y_t):
        continue

    total_cost += a * 3
    total_cost += b


print(total_cost)
