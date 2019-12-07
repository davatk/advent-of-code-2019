from typing import List, Optional


def parse_instruction(instruction_num: int) -> List[int]:
    opcode = instruction_num % 100
    instruction_num = (instruction_num - opcode) / 100
    instruction_parts = [opcode]
    for _ in range(3):
        instruction_parts.append(instruction_num % 10)
        instruction_num = (instruction_num - instruction_parts[-1]) / 10
    return instruction_parts


class IntcodeComputer:
    def __init__(self, program: List[int]):
        self.program = program[:]
        self.outputs = []
        self.ptr = 0

    def run(self, inp: Optional[int] = None) -> bool:
        """
        We run until we
        a) need an input (return False), or
        b) halt (return True)
        """
        while self.program[self.ptr] != 99:
            opcode, param_mode1, param_mode2, dest_mode = parse_instruction(self.program[self.ptr])
            ptr_increment = 2
            if opcode in [1, 2, 5, 6, 7, 8]:
                if param_mode1:
                    arg1 = self.program[self.ptr+1]
                else:
                    arg1 = self.program[self.program[self.ptr+1]]
                if param_mode2:
                    arg2 = self.program[self.ptr+2]
                else:
                    arg2 = self.program[self.program[self.ptr+2]]
                ptr_increment = 3
            if opcode in [1, 2, 7, 8]:
                dest = self.ptr + 3 if dest_mode else self.program[self.ptr+3]
                ptr_increment = 4

            if opcode == 1:
                self.program[dest] = arg1 + arg2
            elif opcode == 2:
                self.program[dest] = arg1 * arg2
            elif opcode == 3:
                if inp is None:
                    return False
                else:
                    self.program[self.program[self.ptr+1]] = inp
                    inp = None
            elif opcode == 4:
                self.outputs.append(self.program[self.program[self.ptr+1]])
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
            else:
                raise ValueError(f"Bad instruction {self.program[self.ptr]} at address {self.ptr}.")

            self.ptr += ptr_increment
        return True

    def run_with_inputs(self, inputs: List[int]) -> List[int]:
        outputs = []
        for inp in inputs:
            rval = self.run(inp)
            if rval == "HALT":
                return outputs
            elif rval != "INPUT":
                outputs.append(rval)


assert parse_instruction(1002) == [2, 0, 1, 0]
assert parse_instruction(3) == [3, 0, 0, 0]
assert parse_instruction(1101) == [1, 1, 1, 0]
