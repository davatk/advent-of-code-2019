from collections import Counter


def good_password(password: int) -> bool:
    digits = [int(c) for c in str(password)]
    never_decreases = all(d <= next_d for d, next_d in zip(digits, digits[1:]))
    has_double = any(count == 2 for count in Counter(digits).values())
    return has_double and never_decreases


assert good_password(112233)
assert not good_password(123444)
assert good_password(111122)


print("Part 1:", len([passwd for passwd in range(172851, 675869) if good_password(passwd)]))
