import math
import re
from itertools import combinations


def _read_input(path):
    output = []
    with open(path, 'r') as f:
        input_str = f.read()
    output.append([[int(s[2:]), 0] for s in re.findall(r'x=-?\d+', input_str)])
    output.append([[int(s[2:]), 0] for s in re.findall(r'y=-?\d+', input_str)])
    output.append([[int(s[2:]), 0] for s in re.findall(r'z=-?\d+', input_str)])
    return output


def apply_gravity(moon_1, moon_2):
    if moon_1[0] < moon_2[0]:
        moon_1[1] += 1
        moon_2[1] -= 1
    elif moon_1[0] > moon_2[0]:
        moon_1[1] -= 1
        moon_2[1] += 1


def get_state(axis):
    return ''.join([str(x) for x in axis])


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


if __name__ == '__main__':
    axes = _read_input('input.txt')
    time_steps = []

    for axis in axes:
        state_dict = {}
        time_step = 0
        while True:
            state = get_state(axis)
            if state_dict.get(state):
                time_steps.append(time_step - 1)
                break
            else:
                state_dict[state] = time_step

            for moon_1, moon_2 in combinations(axis, 2):
                apply_gravity(moon_1, moon_2)
            for moon in axis:
                moon[0] = sum(moon)

            time_step += 1

    print(lcm(lcm(time_steps[0], time_steps[1]), time_steps[2]))
