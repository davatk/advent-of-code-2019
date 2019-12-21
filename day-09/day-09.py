from intcode_computer import IntcodeComputer

with open("input.txt") as f:
    program = [int(num) for num in f.read().strip().split(",")]
    computer1 = IntcodeComputer(program)
    computer1.run(1)
    print("Part 1:", computer1.outputs[-1])
    computer2 = IntcodeComputer(program)
    computer2.run(2)
    print("Part 2:", computer2.outputs[-1])
