import re
from itertools import combinations


def _read_input(path):
    output = []
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    for line in lines:
        output.append({
            'pos': [int(s) for s in re.findall(r'-?\d+', line)],
            'vel': [0, 0, 0]
        })
    return output


def apply_gravity(moon_1, moon_2):
    for i in range(3):
        if moon_1['pos'][i] < moon_2['pos'][i]:
            moon_1['vel'][i] += 1
            moon_2['vel'][i] -= 1
        elif moon_1['pos'][i] > moon_2['pos'][i]:
            moon_1['vel'][i] -= 1
            moon_2['vel'][i] += 1


def moon_energy(moon):
    pot_energy = sum([abs(coord) for coord in moon['pos']])
    kin_energy = sum([abs(coord) for coord in moon['vel']])
    return pot_energy * kin_energy


if __name__ == '__main__':
    moons = _read_input('input.txt')
    time_steps = 1000

    for time_step in range(time_steps):
        for moon_1, moon_2 in combinations(moons, 2):
            apply_gravity(moon_1, moon_2)
        for moon in moons:
            moon['pos'] = [sum(x) for x in zip(moon['pos'], moon['vel'])]

    tot_energy = sum([moon_energy(moon) for moon in moons])
    print(tot_energy)
