from dataclasses import dataclass
from itertools import batched
import re


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
