from collections import defaultdict
from intcode_computer import IntcodeComputer
from matplotlib import pyplot as plt


def update_position(position, direction):
    return {0: (position[0], position[1] + 1),  # N
            1: (position[0] + 1, position[1]),  # E
            2: (position[0], position[1] - 1),  # S
            3: (position[0] - 1, position[1]),  # W
            }[direction]


def paint_hull(program, start_color):
    computer = IntcodeComputer(program)
    # NESW
    direction = 0
    position = (0, 0)
    panel_colors = defaultdict(int)
    panel_colors[position] = start_color
    panels_painted = 1

    def new_direction(turn_right: int):
        if turn_right:
            return (direction + 1) % 4
        else:
            return (direction - 1) % 4

    while not computer.run(panel_colors[position]):
        paint_color = computer.outputs[-2]
        turn_right = computer.outputs[-1]
        panel_colors[position] = paint_color
        direction = new_direction(turn_right)
        position = update_position(position, direction)
        if position not in panel_colors:
            panels_painted += 1

    return panels_painted, panel_colors


with open("input.txt") as f:
    program = [int(n) for n in f.read().strip().split(",")]
    panels_painted, _ = paint_hull(program, start_color=0)
    print("Part 1:", panels_painted)

    # Part 2
    _, panel_colors = paint_hull(program, start_color=1)
    positions = panel_colors.keys()
    x_vals, y_vals = zip(*positions)
    start_x, end_x = min(x_vals), max(x_vals) + 1
    start_y, end_y = min(y_vals), max(y_vals) + 1
    color_arr = [[panel_colors[(x, y)] for x in (range(start_x, end_x))]
                 for y in reversed(range(start_y, end_y))]
    plt.imshow(color_arr)
    plt.show()
