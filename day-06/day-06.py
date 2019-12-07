from typing import Tuple, Dict, DefaultDict, Set, List
from collections import defaultdict, deque


def parse_orbit_graphs(orbits_str: List[str]) -> Tuple[Dict[str, str], DefaultDict[str, Set[str]]]:
    directed_orbits = dict()
    undirected_orbits = defaultdict(set)
    for line in orbits_str:
        orbitee, orbiter = line.strip().split(")")
        undirected_orbits[orbiter].add(orbitee)
        undirected_orbits[orbitee].add(orbiter)
        assert orbiter not in directed_orbits
        directed_orbits[orbiter] = orbitee
    return directed_orbits, undirected_orbits


def total_orbits(orbits: Dict[str, str]) -> int:
    total = 0
    for orbiter, orbitee in orbits.items():
        while orbiter != "COM":
            total += 1
            orbiter = orbits[orbiter]
    return total


def distance_to_santa(orbits: DefaultDict[str, Set[str]]) -> int:
    # -1 because we start from our location, rather than the object we're orbiting
    queue = deque([("YOU", -1)])
    planets_seen = {"YOU"}
    while queue:
        cur_planet, distance = queue.popleft()
        for neighb in orbits[cur_planet]:
            if neighb == "SAN":
                return distance
            if neighb not in planets_seen:
                queue.append((neighb, distance + 1))
                planets_seen.add(neighb)
    raise ValueError("Christmas is cancelled.")


TEST_CASE2 = "COM)B B)C C)D D)E E)F B)G G)H D)I E)J J)K K)L K)YOU I)SAN".split()
TEST_CASE1 = "COM)B B)C C)D D)E E)F B)G G)H D)I E)J J)K K)L""".split()

assert total_orbits(parse_orbit_graphs(TEST_CASE1)[0]) == 42
assert distance_to_santa(parse_orbit_graphs(TEST_CASE2)[1]) == 4

with open("input.txt") as f:
    directed_orbits, undirected_orbits = parse_orbit_graphs(f.readlines())
    print("Part 1:", total_orbits(directed_orbits))
    print("Part 2:", distance_to_santa(undirected_orbits))
