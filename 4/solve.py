def is_valid_1(n):
    digits = str(n)
    return sorted(digits) == list(digits) and len(set(digits)) < len(digits)

print('Part 1:', sum(is_valid_1(x) for x in range(372304, 847061)))


from collections import Counter

def is_valid_2(n):
    digits = str(n)
    return sorted(digits) == list(digits) and 2 in Counter(digits).values()

print('Part 2:', sum(is_valid_2(x) for x in range(372304, 847061)))
