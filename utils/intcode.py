from queue import Queue
from threading import Thread, Event


class GrowingList(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0] * (index + 1 - len(self)))
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        if index >= len(self):
            self.extend([0] * (index + 1 - len(self)))
        return list.__getitem__(self, index)


class IntCode(Thread):
    STOP_CODE = 99
    ADD_CODE = 1
    MULTIPLY_CODE = 2
    INPUT_CODE = 3
    OUTPUT_CODE = 4
    JUMP_IF_TRUE_CODE = 5
    JUMP_IF_FALSE_CODE = 6
    LESS_THAN_CODE = 7
    EQUALS_CODE = 8
    ADJUST_RELATIVE_BASE_CODE = 9

    POSITION_MODE = 0
    IMMEDIATE_MODE = 1
    RELATIVE_MODE = 2

    def __init__(self, input_file):
        super().__init__()
        self.program = GrowingList()
        with open(input_file, 'r') as f:
            for i in f.read().strip().split(','):
                self.program.append(i)
        self.pointer = 0
        self.relative_base = 0
        self.op_code = None
        self.input = Queue()
        self.output = Queue()

    def _get_param_modes(self, nbr_of_params, code):
        return [int(code[-3 - i]) for i in range(nbr_of_params)]

    def _get_params(self, param_modes, write_param_idx=None):
        params = []
        for i, param_mode in enumerate(param_modes):
            if param_mode == self.IMMEDIATE_MODE or i == write_param_idx:
                params.append(int(self.program[self.pointer + i + 1]))
            elif param_mode == self.POSITION_MODE:
                params.append(int(self.program[int(self.program[self.pointer + i + 1])]))
            elif param_mode == self.RELATIVE_MODE:
                params.append(int(self.program[int(self.program[self.pointer + i + 1]) + self.relative_base]))
        return params

    def _write(self, param, param_mode, value):
        if param_mode == self.POSITION_MODE:
            self.program[param] = value
        elif param_mode == self.RELATIVE_MODE:
            self.program[param + self.relative_base] = value

    def run(self):
        while True:
            code = str(self.program[self.pointer]).zfill(5)
            self.op_code = int(code[-2:])

            if self.op_code == self.ADD_CODE:
                param_modes = self._get_param_modes(3, code)
                params = self._get_params(param_modes, write_param_idx=2)
                value = params[0] + params[1]
                self._write(params[2], param_modes[2], value)
                self.pointer += 4

            elif self.op_code == self.MULTIPLY_CODE:
                param_modes = self._get_param_modes(3, code)
                params = self._get_params(param_modes, write_param_idx=2)
                value = params[0] * params[1]
                self._write(params[2], param_modes[2], value)
                self.pointer += 4

            elif self.op_code == self.INPUT_CODE:
                param_modes = self._get_param_modes(1, code)
                params = self._get_params(param_modes, write_param_idx=0)
                value = self.input.get()
                self._write(params[0], param_modes[0], value)
                self.pointer += 2

            elif self.op_code == self.OUTPUT_CODE:
                param_modes = self._get_param_modes(1, code)
                params = self._get_params(param_modes)
                self.output.put(params[0])
                self.pointer += 2

            elif self.op_code == self.JUMP_IF_TRUE_CODE:
                param_modes = self._get_param_modes(2, code)
                params = self._get_params(param_modes)
                if params[0] != 0:
                    self.pointer = params[1]
                else:
                    self.pointer += 3

            elif self.op_code == self.JUMP_IF_FALSE_CODE:
                param_modes = self._get_param_modes(2, code)
                params = self._get_params(param_modes)
                if params[0] == 0:
                    self.pointer = params[1]
                else:
                    self.pointer += 3

            elif self.op_code == self.LESS_THAN_CODE:
                param_modes = self._get_param_modes(3, code)
                params = self._get_params(param_modes, write_param_idx=2)
                value = 1 if params[0] < params[1] else 0
                self._write(params[2], param_modes[2], value)
                self.pointer += 4

            elif self.op_code == self.EQUALS_CODE:
                param_modes = self._get_param_modes(3, code)
                params = self._get_params(param_modes, write_param_idx=2)
                value = 1 if params[0] == params[1] else 0
                self._write(params[2], param_modes[2], value)
                self.pointer += 4

            elif self.op_code == self.ADJUST_RELATIVE_BASE_CODE:
                param_modes = self._get_param_modes(1, code)
                params = self._get_params(param_modes)
                self.relative_base += params[0]
                self.pointer += 2

            elif self.op_code == self.STOP_CODE:
                # self.run_condition.notify_all()
                # self.run_condition.release()
                break

            else:
                print(self.op_code)
                break
