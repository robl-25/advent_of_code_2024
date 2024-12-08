def is_valid(numbers, current_result, target_result):
    if not numbers:
        return current_result == target_result

    current_number = numbers[0]

    if current_result == 0:
        current_result_mult = 1
    else:
        current_result_mult = current_result

    return (
        is_valid(numbers[1:], current_result + current_number, target_result) or
        is_valid(numbers[1:], current_result_mult * current_number, target_result)
    )

with open('input.txt') as f:
    data = f.readlines()

total = 0

for equation in data:
    result, numbers = equation.split(':')
    
    result = int(result)
    numbers = [int(number) for number in numbers.split()]

    if is_valid(tuple(numbers), 0, result):
        total += result

print(total)
