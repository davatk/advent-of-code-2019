from typing import List, Tuple


def get_points(route: List[str]) -> List[Tuple[int, int]]:
    points = []
    x, y = 0, 0
    for move in route:
        direction = move[0]
        for _ in range(int(move[1:])):
            if direction == "R":
                x += 1
            elif direction == "L":
                x -= 1
            elif direction == "U":
                y += 1
            elif direction == "D":
                y -= 1
            else:
                raise ValueError(f"Unknown direction: {direction}")
            points.append((x, y))
    return points


def manhattan_distance(start: Tuple[int, int], end: Tuple[int, int]) -> int:
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def distance_to_closest_intersection(route1: List[str], route2: List[str]) -> int:
    intersections = set(get_points(route1)) & set(get_points(route2))
    return min(manhattan_distance((0, 0), intersection) for intersection in intersections)


def fewest_steps(route1: List[str], route2: List[str]) -> int:
    route1_points = get_points(route1)
    route2_points = get_points(route2)
    intersections = set(route1_points) & set(route2_points)

    def steps_needed(intersection: Tuple[int, int]) -> int:
        return route1_points.index(intersection) + route2_points.index(intersection) + 2

    return min(steps_needed(intersection) for intersection in intersections)


examples = [("R8,U5,L5,D3", "U7,R6,D4,L4", 6, 30),
            ("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83", 159, 610),
            ("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
             "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7", 135, 410)]

for route1_str, route2_str, distance, steps in examples:
    route1 = route1_str.split(",")
    route2 = route2_str.split(",")
    assert distance_to_closest_intersection(route1, route2) == distance
    assert fewest_steps(route1, route2) == steps

with open("input.txt") as f:
    routes = f.read().split("\n")
    route1, route2 = routes[0].split(","), routes[1].split(",")
    print("Part 1:", distance_to_closest_intersection(route1, route2))
    print("Part 2:", fewest_steps(route1, route2))
