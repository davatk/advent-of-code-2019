"""
Fuel required to launch a given module is based on its mass.
Specifically, to find the fuel required for a module, take its mass, divide by three, round down,
and subtract 2.

For example:

For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
For a mass of 1969, the fuel required is 654.
For a mass of 100756, the fuel required is 33583.
The Fuel Counter-Upper needs to know the total fuel requirement.
To find it, individually calculate the fuel needed for the mass of each module (your puzzle input),
then add together all the fuel values.

What is the sum of the fuel requirements for all of the modules on your spacecraft?
"""

def fuel_required(module_mass: int) -> int:
    return (module_mass // 3) - 2

assert fuel_required(12) == 2
assert fuel_required(14) == 2
assert fuel_required(1969) == 654
assert fuel_required(100756) == 33583

with open("input.txt") as f:
    print("Part 1:", sum(fuel_required(int(line)) for line in f))


### Part 2 ###

def additional_fuel_required(mass: int) -> int:
    needed_fuel = (mass // 3) - 2
    total = 0
    while needed_fuel > 0:
        total += needed_fuel
        needed_fuel = (needed_fuel // 3) - 2
    return total


assert additional_fuel_required(14) == 2
assert additional_fuel_required(1969) == 966
assert additional_fuel_required(100756) == 50346
assert additional_fuel_required(5) == 0

with open("input.txt") as f:
    print("Part 2:", sum(additional_fuel_required(int(line)) for line in f))
