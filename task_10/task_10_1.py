import math
import copy
from itertools import combinations
from tqdm import tqdm


def read_input(path):
    with open(path, 'r') as f:
        output = f.read().splitlines()
    return output


def input_2_coords(lines):
    coords = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '#':
                coords.append((j, i))
    return coords


def dist(coord_1, coord_2):
    x1, y1 = coord_1
    x2, y2 = coord_2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def pop_list(list, elms):
    list = copy.deepcopy(list)
    for elm in elms:
        list.remove(elm)
    return list


if __name__ == '__main__':
    lines = read_input('input.txt')
    coords = input_2_coords(lines)

    viewable_asteroids = {coord: 0 for coord in coords}
    for ast1, ast2 in tqdm(combinations(coords, 2)):
        blocking = False
        for block in pop_list(coords, [ast1, ast2]):
            blocking = dist(ast1, block) + dist(ast2, block) - dist(ast1, ast2) < 1e-6
            if blocking:
                break
        if not blocking:
            viewable_asteroids[ast1] += 1
            viewable_asteroids[ast2] += 1

    print(max(viewable_asteroids, key=(lambda key: viewable_asteroids[key])))
    print(max(viewable_asteroids.values()))
