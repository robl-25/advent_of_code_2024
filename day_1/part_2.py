from collections import Counter

list_1 = []
list_2 = []

with open('input.txt') as f:
    lines = f.readlines()

for line in lines:
    list_1_item, list_2_item = [int(l) for l in line.split()]

    list_1.append(list_1_item)
    list_2.append(list_2_item)

counter = Counter(list_2)

total = sum(location_id * counter[location_id] for location_id in list_1)
print(total)