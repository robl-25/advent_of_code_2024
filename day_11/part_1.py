from functools import cache


@cache
def blink(stone_value):
    if stone_value == 0:
        return (1,)

    if len(str(stone_value)) % 2 == 0:
        value_str = str(stone_value)
        middle_index = len(value_str) // 2
        
        value_a = value_str[:middle_index] 
        value_b = value_str[middle_index:]

        stone_value = value_a

        return (int(value_a), int(value_b))
    
    return (stone_value * 2024,)


with open('input.txt') as f:
    stones = [int(i) for i in f.read().strip().split(' ')]

aux_stones = []

for i in range(25):
    for stone in stones:
        aux_stones.extend(blink(stone))

    stones = aux_stones
    aux_stones = []

print(len(stones))
