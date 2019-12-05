from typing import List


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


with open("input.txt") as f:
    program = [int(i) for i in f.read().strip().split(",")]
    print("Part 1: ", run_intcode(program, inputs=[1])[-1])  # 7286649
    print("Part 2: ", run_intcode(program, inputs=[5])[-1])
