def good_password(password: int) -> bool:
    digits = [int(c) for c in str(password)]
    never_decreases = True
    has_double = False
    for digit, next_digit in zip(digits, digits[1:]):
        if digit == next_digit:
            has_double = True
        if next_digit < digit:
            never_decreases = False
    return has_double and never_decreases


assert good_password(111111)
assert not good_password(223450)
assert not good_password(123789)


print("Part 1:", len([passwd for passwd in range(172851, 675869) if good_password(passwd)]))
