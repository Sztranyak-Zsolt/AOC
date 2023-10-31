from typing import Self


class InputError(Exception):
    pass


class UnknownFunctionCode(Exception):
    pass


class CIntCode:
    def __init__(self, p_init_memory_list: list[int] | None = None,
                 p_init_input_list: list[int] | None = None):
        self.opcode_func = {1: self.add, 2: self.mul, 99: self.halt,
                            3: self.input, 4: self.output,
                            5: self.jump_if_true, 6: self.jump_if_false,
                            7: self.less_than, 8: self.equals,
                            9: self.relative_base_offset}
        if p_init_memory_list is None:
            self.init_memory_list: list[int] = []
        else:
            self.init_memory_list = p_init_memory_list.copy()
        self.program_code_dict = {i: v for i, v in enumerate(self.init_memory_list)}

        self.instruction_pointer = 0
        self.relative_base = 0
        self.program_finished = False
        if p_init_input_list is None:
            self.init_input_list: list[int] = []
        else:
            self.init_input_list = p_init_input_list.copy()
        self.input_list = self.init_input_list.copy()
        self.output_list: list[int] = []

    @property
    def output_text(self) -> str:
        return ''.join([chr(act_code) for act_code in self.output_list])

    def set_input_from_text_list(self, p_input_text_list: list[str], p_extend_existing: bool = False):
        rl = []
        for act_text in p_input_text_list:
            for act_char in act_text:
                rl.append(ord(act_char))
            rl.append(10)
        if not p_extend_existing:
            self.input_list.clear()
        self.input_list += rl

    def reset_program(self):
        self.program_code_dict = {i: v for i, v in enumerate(self.init_memory_list)}
        self.instruction_pointer = 0
        self.relative_base = 0
        self.input_list.clear()
        self.input_list += self.init_input_list
        self.output_list.clear()
        self.program_finished = False

    def read_memory(self, p_mode: int = 0) -> int:
        act_memory_value = self.program_code_dict.get(self.instruction_pointer, 0)
        self.instruction_pointer += 1
        if p_mode == 0:
            return self.program_code_dict.get(act_memory_value, 0)
        elif p_mode == 1:
            return act_memory_value
        elif p_mode == 2:
            return self.program_code_dict.get(act_memory_value + self.relative_base, 0)

    def write_memory(self, p_value: int, p_mode: int = 0):
        act_memory_value = self.program_code_dict.get(self.instruction_pointer, 0)
        self.instruction_pointer += 1
        if p_mode == 0:
            self.program_code_dict[act_memory_value] = p_value
        elif p_mode == 1:
            self.program_code_dict[self.program_code_dict.get(act_memory_value, 0)] = p_value
        elif p_mode == 2:
            self.program_code_dict[act_memory_value + self.relative_base] = p_value

    def add(self, p_param_list: list[int]):
        self.write_memory(self.read_memory(p_param_list[0]) + self.read_memory(p_param_list[1]), p_param_list[2])

    def mul(self, p_param_list: list[int]):
        self.write_memory(self.read_memory(p_param_list[0]) * self.read_memory(p_param_list[1]), p_param_list[2])

    def input(self, p_param_list: list[int]):
        if not self.input_list:
            self.instruction_pointer -= 1
            raise InputError
        self.write_memory(self.input_list.pop(0), p_param_list[0])

    def output(self, p_param_list: list[int]):
        self.output_list.append(self.read_memory(p_param_list[0]))

    def jump_if_true(self, p_param_list: list[int]):
        mem1_value = self.read_memory(p_param_list[0])
        mem2_value = self.read_memory(p_param_list[1])
        if mem1_value != 0:
            self.instruction_pointer = mem2_value

    def jump_if_false(self, p_param_list: list[int]):
        mem1_value = self.read_memory(p_param_list[0])
        mem2_value = self.read_memory(p_param_list[1])
        if mem1_value == 0:
            self.instruction_pointer = mem2_value

    def less_than(self, p_param_list: list[int]):
        if self.read_memory(p_param_list[0]) < self.read_memory(p_param_list[1]):
            self.write_memory(1, p_param_list[2])
        else:
            self.write_memory(0, p_param_list[2])

    def equals(self, p_param_list: list[int]):
        if self.read_memory(p_param_list[0]) == self.read_memory(p_param_list[1]):
            self.write_memory(1, p_param_list[2])
        else:
            self.write_memory(0, p_param_list[2])

    def relative_base_offset(self, p_param_list: list[int]):
        self.relative_base += self.read_memory(p_param_list[0])

    def halt(self, p_param_list: list[int]):
        self.instruction_pointer -= 1
        self.program_finished = True

    def execute_next_instruction(self):
        act_op_code = self.read_memory(1)
        act_function_code = act_op_code % 100
        if act_function_code not in self.opcode_func:
            self.instruction_pointer -= 1
            raise UnknownFunctionCode(f'Unknown function code: {act_function_code}')
        param_modes = [act_op_code // 100 % 10, act_op_code // 1000 % 10, act_op_code // 10000 % 10]
        self.opcode_func[act_function_code](param_modes)

    def run_program(self):
        while not self.program_finished:
            self.execute_next_instruction()

    def run_until_next_outputs(self, p_output_count: int = 1):
        while not self.program_finished and len(self.output_list) != p_output_count:
            self.execute_next_instruction()

    def run_until_next_input_needed(self):
        while not self.program_finished:
            try:
                self.execute_next_instruction()
            except InputError:
                return

    def __copy__(self) -> Self:
        new_instance = self.__class__()
        new_instance.init_memory_list = self.init_memory_list.copy()
        new_instance.program_code_dict = self.program_code_dict.copy()
        new_instance.instruction_pointer = self.instruction_pointer
        new_instance.relative_base = self.relative_base
        new_instance.program_finished = False
        new_instance.init_input_list = self.init_input_list.copy()
        new_instance.input_list = self.input_list.copy()
        new_instance.output_list = self.output_list.copy()

        return new_instance

    @property
    def prog_state_code(self) -> str:
        return f'{self.instruction_pointer} {self.relative_base} ' \
               f'{"".join([str(x) for x in self.program_code_dict.values()])} ' \
               f'{"".join([str(x) for x in self.output_list])} ' \
               f'{"".join([str(x) for x in self.output_list])}'

    def add_input(self, p_value: int):
        self.input_list.append(p_value)


def main():
    pass


if __name__ == '__main__':
    main()
