import math


def read_input(path):
    with open(path, 'r') as f:
        output = f.read().splitlines()
    return output


def input_2_cart_coords(lines):
    coords = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '#':
                coords.append((j, i))
    return coords


def origo_2_laser(cart_coords, laser_pos):
    x0, y0 = laser_pos
    return [(x - x0, y - y0) for x, y in cart_coords]


def cart_2_polar(cart_coords):
    polar_coords = [(math.sqrt(x**2 + y**2), math.atan2(x, y)) for x, y in cart_coords]
    return polar_coords


if __name__ == '__main__':
    lines = read_input('input.txt')
    cart_coords = input_2_cart_coords(lines)
    laser_pos = (30, 34)
    trans_cart_coords = origo_2_laser(cart_coords, laser_pos)
    polar_coords = cart_2_polar(trans_cart_coords)
    polar_coords.sort(key=lambda key: (-key[1], key[0]))
    for i in range(len(polar_coords)):
        if polar_coords[i][1] == polar_coords[-1][1] or i == len(polar_coords) - 1:
            break
        j = i + 1
        while polar_coords[j][1] == polar_coords[i][1]:
            polar_coords.append(polar_coords.pop(j))

    r, theta = polar_coords[199]
    x = r * math.sin(theta) + laser_pos[0]
    y = r * math.cos(theta) + laser_pos[1]
    print(x * 100 + y)
