from typing import List
from operator import add, mul

def parse(program_str: str) -> List[int]:
    return [int(i) for i in program_str.split(",")]

def run_intcode(program: List[int], noun: int = None, verb: int = None) -> List[int]:
    program = program[:]
    if noun:
        program[1] = noun
    if verb:
        program[2] = verb
    pointer = 0
    while program[pointer] != 99:
        op = add if program[pointer] == 1 else mul
        program[program[pointer+3]] = op(program[program[pointer+1]], program[program[pointer+2]])
        pointer += 4
    return program

assert run_intcode(parse("1,0,0,0,99")) == [2,0,0,0,99]
assert run_intcode(parse("2,3,0,3,99")) == [2,3,0,6,99]
assert run_intcode(parse("2,4,4,5,99,0")) == [2,4,4,5,99,9801]
assert run_intcode(parse("1,1,1,4,99,5,6,0,99")) == [30,1,1,4,2,5,6,0,99]
assert run_intcode(parse("1,9,10,3,2,3,11,0,99,30,40,50")) == [3500,9,10,70,2,3,11,0,99,30,40,50]

with open("input.txt") as f:
    program = parse(f.read().strip())
    print("Part 1:", run_intcode(list(program), 12, 2)[0])
    for noun in range(100):
        for verb in range(100):
            if run_intcode(program, noun, verb)[0] == 19690720:
                print("Part 2:", noun * 100 + verb)
                break
