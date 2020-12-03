from utils.intcode import IntCode


def print_panels(painted_panels):
    x_coords = [pos[0] for pos in painted_panels.keys()]
    y_coords = [pos[1] for pos in painted_panels.keys()]
    x_max, x_min = max(x_coords), min(x_coords)
    y_max, y_min = max(y_coords), min(y_coords)

    white_color = '#'
    black_color = '.'
    panel_matrix = [[black_color] * (x_max - x_min + 1) for _ in range(y_max - y_min + 1)]
    for pos, color_ind in painted_panels.items():
        if color_ind == 1:
            panel_matrix[pos[1] - y_min][pos[0] - x_min] = white_color

    panel_matrix.reverse()
    print('\n'.join([''.join(['{:2}'.format(item) for item in row]) for row in panel_matrix]))


if __name__ == '__main__':
    painted_panels = {}
    pos = (0, 0)
    dir = (0, 1)
    color_output = True
    intcode_prog = IntCode('input.txt')
    intcode_prog.start()

    painted_panels[pos] = 1

    while intcode_prog.op_code != intcode_prog.STOP_CODE:
        panel_color = 0 if pos not in painted_panels.keys() else painted_panels[pos]
        intcode_prog.input.put(panel_color)

        painted_panels[pos] = intcode_prog.output.get()

        turn = intcode_prog.output.get()
        dir = (-dir[1], dir[0]) if turn == 0 else (dir[1], -dir[0])
        pos = (pos[0] + dir[0], pos[1] + dir[1])

    intcode_prog.join()
    print_panels(painted_panels)
