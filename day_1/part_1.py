list_1 = []
list_2 = []

with open('input.txt') as f:
    lines = f.readlines()

for line in lines:
    list_1_item, list_2_item = [int(l) for l in line.split()]

    list_1.append(list_1_item)
    list_2.append(list_2_item)

list_1.sort()
list_2.sort()

distances = sum(abs(l1 - l2)  for l1, l2 in zip(list_1, list_2))

print(distances)