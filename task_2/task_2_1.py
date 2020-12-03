from utils.intcode import IntCode

if __name__ == '__main__':
    intcode_prog = IntCode('input.txt')
    print(intcode_prog.run([12, 2]))
