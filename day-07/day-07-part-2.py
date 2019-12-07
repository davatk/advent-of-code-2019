from typing import List
import itertools as it
from intcode_computer import IntcodeComputer


def thruster_signal(program: List[int], phase_setting: List[int]) -> int:
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

with open("input.txt") as f:
    program = [int(n) for n in f.read().strip().split(",")]
    print("Part 2:", max_thruster_signal(program))
