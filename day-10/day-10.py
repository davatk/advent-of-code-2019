from typing import List, Tuple, Iterator, DefaultDict
import math
from collections import defaultdict, deque


def parse(puzzle: str) -> List[str]:
    return puzzle.strip().split("\n")


def get_asteroids(asteroid_field) -> List[Tuple[int, int]]:
    field_width = len(asteroid_field)
    return [(x, y) for x in range(field_width) for y in range(field_width)
            if asteroid_field[y][x] == '#']


def displacement_vector(start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[float, float]:
    # just using the polar coordinates
    rise = end[0] - start[0]
    run = end[1] - start[1]
    phi = math.atan2(-run, -rise)
    r = math.sqrt(rise**2 + run**2)
    return round(phi, 10), round(r, 10)


def asteroids_detected(center: Tuple[int, int], asteroid_field: List[str]) -> int:
    lines_of_sight = {displacement_vector(center, target)[0]
                      for target in get_asteroids(asteroid_field) if target != center}
    return len(lines_of_sight)


def best_location(asteroid_field: List[str]) -> Tuple[int, int]:
    asteroids = get_asteroids(asteroid_field)
    return max(asteroids,
               key=lambda asteroid: asteroids_detected(asteroid, asteroid_field))


def vaporized_asteroids(asteroid_field: List[str]) -> Iterator[Tuple[int, int]]:
    asteroids = get_asteroids(asteroid_field)
    laser = best_location(asteroid_field)
    asteroids_left: DefaultDict[float, List[Tuple[float, Tuple[int, int]]]] = defaultdict(list)
    for asteroid in asteroids:
        if asteroid != laser:
            phi, r = displacement_vector(laser, asteroid)
            asteroids_left[phi].append((r, asteroid))
    for los_asteroids in asteroids_left.values():
        # reverse, since we'll be popping off the end
        los_asteroids.sort(reverse=True)

    # We start at 12 o'clock rather than 3, and go clockwise, when lasering stuff:
    def transformed_phi(phi: float) -> float:
        return ((5 * math.pi / 2) - phi) % (2 * math.pi)

    sorted_phis = sorted(asteroids_left, key=transformed_phi, reverse=True)

    while asteroids_left:
        for phi in sorted_phis:
            if phi not in asteroids_left:
                continue
            los_asteroids = asteroids_left[phi]
            # we yield the next nearest (by `r`) asteroid
            yield los_asteroids.pop()[1]
            if not los_asteroids:
                # we've exhausted this line of sight
                asteroids_left.pop(phi)


test_case1 = parse(""".#..#
.....
#####
....#
...##
""")

test_case2 = parse("""......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""")

test_case3 = parse("""#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
""")

test_case4 = parse(""".#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
""")

test_case5 = parse(""".#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""")

assert (best_loc1 := best_location(test_case1)) == (3, 4)
assert asteroids_detected(best_loc1, test_case1) == 8
assert (best_loc2 := best_location(test_case2)) == (5, 8)
assert asteroids_detected(best_loc2, test_case2) == 33
assert (best_loc3 := best_location(test_case3)) == (1, 2)
assert asteroids_detected(best_loc3, test_case3) == 35
assert (best_loc4 := best_location(test_case4)) == (6, 3)
assert asteroids_detected(best_loc4, test_case4) == 41
assert (best_loc5 := best_location(test_case5)) == (11, 13)
assert asteroids_detected(best_loc5, test_case5) == 210

ideal_order = [(0, (11,12)),
               (1, (12,1)),
               (2, (12,2)),
               (9, (12,8)),
               (19, (16,0)),
               (49, (16,9)),
               (99, (10,16)),
               (198, (9,6)),
               (199, (8,2)),
               (200, (10,9)),
               (298, (11,1))]

actual_order = list(vaporized_asteroids(test_case5))

for vapor_idx, asteroid_loc in ideal_order:
    assert actual_order[vapor_idx] == asteroid_loc

with open("input.txt") as f:
    puzzle_input = parse(f.read().strip())
    print("Part 1:", asteroids_detected(best_location(puzzle_input), puzzle_input))
    print("Part 2:", list(vaporized_asteroids(puzzle_input))[199])
