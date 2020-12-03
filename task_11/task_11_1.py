from utils.intcode import IntCode

if __name__ == '__main__':
    painted_panels = {}
    pos = (0, 0)
    dir = (0, 1)
    color_output = True
    intcode_prog = IntCode('input.txt')
    intcode_prog.start()

    while intcode_prog.op_code != intcode_prog.STOP_CODE:

        panel_color = 0 if pos not in painted_panels.keys() else painted_panels[pos]
        intcode_prog.input.put(panel_color)

        painted_panels[pos] = intcode_prog.output.get()

        turn = intcode_prog.output.get()
        dir = (-dir[1], dir[0]) if turn == 0 else (dir[1], -dir[0])
        pos = (pos[0] + dir[0], pos[1] + dir[1])

    intcode_prog.join()
    print(len(painted_panels))
