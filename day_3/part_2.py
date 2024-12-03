import re

regex = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)|(do|don\'t)\(\)')

with open('input.txt') as f:
    jumbled_memory = f.read()

enabled = True
total = 0

for a, b, operation in regex.findall(jumbled_memory):
    if operation == 'do':
        enabled = True
    
    if operation == "don't":
        enabled = False

    if enabled and operation == '':
        total += int(a) * int(b)

print(total)
