from typing import List
import itertools as it


def parse_instruction(instruction_num: int) -> List[int]:
    opcode = instruction_num % 100
    instruction_num = (instruction_num - opcode) / 100
    instruction_parts = [opcode]
    for _ in range(3):
        instruction_parts.append(instruction_num % 10)
        instruction_num = (instruction_num - instruction_parts[-1]) / 10
    return instruction_parts

assert parse_instruction(1002) == [2, 0, 1, 0]
assert parse_instruction(3) == [3, 0, 0, 0]
assert parse_instruction(1101) == [1, 1, 1, 0]


def run_intcode(program: List[int], inputs: List[int] = None) -> List[int]:
    program = program[:]
    if inputs:
        inputs = list(reversed(inputs))
    outputs = []
    pointer = 0
    while program[pointer] != 99:
        opcode, param_mode1, param_mode2, dest_mode = parse_instruction(program[pointer])
        pointer_increment = 2
        if opcode in [1, 2, 5, 6, 7, 8]:
            arg1 = program[pointer+1] if param_mode1 else program[program[pointer+1]]
            arg2 = program[pointer+2] if param_mode2 else program[program[pointer+2]]
            pointer_increment = 3
        if opcode in [1, 2, 7, 8]:
            dest = pointer + 3 if dest_mode else program[pointer+3]
            pointer_increment = 4

        if opcode == 1:
            program[dest] = arg1 + arg2
        elif opcode == 2:
            program[dest] = arg1 * arg2
        elif opcode == 3:
            program[program[pointer+1]] = inputs.pop()
        elif opcode == 4:
            outputs.append(program[program[pointer+1]])
        elif opcode == 5:
            if arg1:
                pointer = arg2
                pointer_increment = 0
        elif opcode == 6:
            if not arg1:
                pointer = arg2
                pointer_increment = 0
        elif opcode == 7:
            program[dest] = 1 if arg1 < arg2 else 0
        elif opcode == 8:
            program[dest] = 1 if arg1 == arg2 else 0
        else:
            raise ValueError(f"Bad instruction {program[pointer]} at address {pointer}.")

        pointer += pointer_increment
    return outputs


def thruster_signal(program: List[int], phase_setting: List[int]) -> int:
    prev_amp_output = 0
    for phase_idx in range(5):
        prev_amp_output = run_intcode(program, [phase_setting[phase_idx], prev_amp_output])[0]
    return prev_amp_output


def max_thruster_signal(program: List[int]) -> int:
    return max(thruster_signal(program, phase_setting)
               for phase_setting in it.permutations(range(5)))


program1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
phase_setting1 = [4,3,2,1,0]
program2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
phase_setting2 = [0,1,2,3,4]
program3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,
            31,99,0,0,0]
phase_setting3 = [1,0,4,3,2]

assert thruster_signal(program1, phase_setting1) == 43210
assert max_thruster_signal(program1) == 43210
assert thruster_signal(program2, phase_setting2) == 54321
assert max_thruster_signal(program2) == 54321
assert thruster_signal(program3, phase_setting3) == 65210
assert max_thruster_signal(program3) == 65210

with open("input.txt") as f:
    program = [int(n) for n in f.read().strip().split(",")]
    print("Part 1:", max_thruster_signal(program))
