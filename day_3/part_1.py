import re

regex = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')

with open('input.txt') as f:
    jumbled_memory = f.read()

total = 0

for a, b in regex.findall(jumbled_memory):
    total += int(a) * int(b)

print(total)
