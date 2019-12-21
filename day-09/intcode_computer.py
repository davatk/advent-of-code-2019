from typing import List, Optional, Tuple, DefaultDict, Sequence
from collections import defaultdict
import itertools as it

Program = DefaultDict[int, int]


def parse_instruction(instruction_num: int) -> List[int]:
    opcode = instruction_num % 100
    instruction_num = (instruction_num - opcode) // 100
    instruction_parts = [opcode]
    for _ in range(3):
        instruction_parts.append(instruction_num % 10)
        instruction_num = (instruction_num - instruction_parts[-1]) // 10
    return instruction_parts


def resolve_arguments(program: Program, ptr: int, rel_base: int) -> Tuple[int, int, int, int]:
    opcode, *param_modes = parse_instruction(program[ptr])

    def resolve_argument(arg_num: int) -> int:
        param_mode = param_modes[arg_num - 1]
        arg_addr = {
            # position mode: "if the param is 50, its value is the value stored at address 50"
            0: program[ptr+arg_num],
            # immediate mode: "if the parameter is 50, its value is simply 50"
            1: ptr + arg_num,
            # relative mode: "given a relative base of 50, a relative mode parameter of -7
            #                 refers to memory address 50 + -7 = 43."
            2: program[ptr+arg_num] + rel_base,
        }[param_mode]

        # If this is the destination, just return the address
        # opcode 3 is input, so it's using its first argument as a destination
        if arg_num == 3 or opcode == 3:
            return arg_addr
        else:
            return program[arg_addr]

    return opcode, resolve_argument(1), resolve_argument(2), resolve_argument(3)


class IntcodeComputer:
    def __init__(self, program: List[int]):
        # We store program as dict from postitons to values.
        self.program: Program = defaultdict(int)
        for idx, val in enumerate(program):
            self.program[idx] = val
        self.outputs: List[int] = []
        self.ptr = 0
        self.relative_base = 0

    def run(self, inp: Optional[int] = None) -> bool:
        """
        We run until we
        a) need an input (return False), or
        b) halt (return True)
        """
        while self.program[self.ptr] != 99:
            opcode, arg1, arg2, dest = resolve_arguments(self.program, self.ptr, self.relative_base)
            if opcode in [1, 2, 7, 8]:
                ptr_increment = 4
            elif opcode in [5, 6]:
                ptr_increment = 3
            else:
                ptr_increment = 2

            if opcode == 1:
                self.program[dest] = arg1 + arg2
            elif opcode == 2:
                self.program[dest] = arg1 * arg2
            elif opcode == 3:
                if inp is None:
                    return False
                else:
                    self.program[arg1] = inp
                    inp = None
            elif opcode == 4:
                self.outputs.append(arg1)
            elif opcode == 5:
                if arg1:
                    self.ptr = arg2
                    ptr_increment = 0
            elif opcode == 6:
                if not arg1:
                    self.ptr = arg2
                    ptr_increment = 0
            elif opcode == 7:
                self.program[dest] = 1 if arg1 < arg2 else 0
            elif opcode == 8:
                self.program[dest] = 1 if arg1 == arg2 else 0
            # relative base offset
            elif opcode == 9:
                self.relative_base += arg1
            else:
                raise ValueError(f"Bad instruction {self.program[self.ptr]} at address {self.ptr}.")

            self.ptr += ptr_increment
        return True


### Tests ###

assert parse_instruction(1002) == [2, 0, 1, 0]
assert parse_instruction(3) == [3, 0, 0, 0]
assert parse_instruction(1101) == [1, 1, 1, 0]


def thruster_signal(program: List[int], phase_setting: Sequence[int]) -> int:
    # first time an amp asks for input, give it the phase signal. After that, it's all signals
    # from previous amps. Halt when the last amp halts.
    amps = [IntcodeComputer(program) for _ in range(5)]
    for amp_idx in range(5):
        amps[amp_idx].run(phase_setting[amp_idx])

    # hacky, but we prime last amp with 0 so first amp will use 0 as input
    amps[4].outputs.append(0)
    for amp_idx in it.cycle(range(5)):
        prev_amp = amps[(amp_idx - 1) % 5]
        amp_halted = amps[amp_idx].run(prev_amp.outputs[-1])
        if amp_halted and amp_idx == 4:
            return amps[amp_idx].outputs[-1]


def max_thruster_signal(program: List[int]) -> int:
    return max(thruster_signal(program, phase_setting)
               for phase_setting in it.permutations(range(5, 10)))


program1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
phase_setting1 = [9,8,7,6,5]
program2 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,
            54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
phase_setting2 = [9,7,8,5,6]

assert thruster_signal(program1, phase_setting1) == 139629729
assert max_thruster_signal(program1) == 139629729
assert thruster_signal(program2, phase_setting2) == 18216
assert max_thruster_signal(program2) == 18216

program3 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
computer3 = IntcodeComputer(program3)
computer3.run()
assert computer3.outputs == program3

computer4 = IntcodeComputer([1102,34915192,34915192,7,4,7,99,0])
computer4.run()
assert len(str(computer4.outputs[-1])) == 16

program5 = [104,1125899906842624,99]
computer5 = IntcodeComputer(program5)
computer5.run()
assert computer5.outputs[-1] == program5[1]


with open("../day-05/input.txt") as f:
    program = [int(i) for i in f.read().strip().split(",")]
    computer6 = IntcodeComputer(program)
    computer6.run(1)
    assert computer6.outputs[-1] == 7286649
    computer7 = IntcodeComputer(program)
    computer7.run(5)
    assert computer7.outputs[-1] == 15724522
