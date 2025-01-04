def backtrack(pattern, towels):
    if not pattern:
        return True

    for towel in towels:
        if pattern.startswith(towel) and backtrack(pattern[len(towel):], towels):
            return True

    return False


with open('input.txt') as f:
    data = f.read()

    towels_data, patterns_data = data.split('\n\n')

    towels = towels_data.strip().split(', ')
    patterns = [l for l in patterns_data.splitlines()]

print(sum(backtrack(pattern, towels) for pattern in patterns))
