from functools import cache

@cache
def blink(stone, n):
    if n == 0:
        return 1

    if stone == 0:
        return blink(1, n - 1)

    stone_str = str(stone)

    if len(stone_str) % 2 == 0:
        middle_index = len(stone_str) // 2
        
        value_a = stone_str[:middle_index] 
        value_b = stone_str[middle_index:]

        stone = value_a

        return (
            blink(int(value_a), n - 1) +
            blink(int(value_b), n - 1)
        )
    
    return blink(stone * 2024, n - 1)
    

with open('input.txt') as f:
    stones = [int(i) for i in f.read().strip().split(' ')]

aux_stones = []

total = sum(blink(stone, 75) for stone in stones)

print(total)
