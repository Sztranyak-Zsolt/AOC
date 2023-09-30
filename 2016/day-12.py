from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CCalculation:
    def __init__(self):
        self.vars = {"a": 0, "b": 0, "c": 0, "d": 0}
        self.instr_list = list()

    def reset_vars(self):
        self.vars = {"a": 0, "b": 0, "c": 0, "d": 0}

    def cpy(self, p_param1: str | int, p_param2: str) -> int:
        if isinstance(p_param1, int):
            self.vars[p_param2] = p_param1
        else:
            self.vars[p_param2] = self.vars[p_param1]
        return 1

    def inc(self, p_param1: str) -> int:
        self.vars[p_param1] += 1
        return 1

    def dec(self, p_param1: str) -> int:
        self.vars[p_param1] -= 1
        return 1

    def jnz(self, p_param1: str | int, p_param2: int) -> int:
        if isinstance(p_param1, int):
            if p_param1 != 0:
                return p_param2
        else:
            if self.vars[p_param1] != 0:
                return p_param2
        return 1

    def add_instruction(self, p_instruction_row: list[int | str]):
        self.instr_list.append([eval(f"self.{p_instruction_row[0]}"), p_instruction_row[1:]])

    def calculate(self):
        act_index = 0
        while True:
            try:
                act_index += self.instr_list[act_index][0](*self.instr_list[act_index][1])
            except IndexError:
                break


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    c = CCalculation()
    for inp_row in yield_input_data(p_input_file_path):
        c.add_instruction(inp_row)

    c.calculate()
    answer1 = c.vars['a']

    c.reset_vars()
    c.vars['c'] = 1
    c.calculate()
    answer2 = c.vars['a']

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 12, solve_puzzle)


if __name__ == '__main__':
    main()
