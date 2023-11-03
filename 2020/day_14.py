from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CMemory:
    def __init__(self):
        self.mem_dict: dict[int, int] = {}
        self.mem_dict2: dict[int, int] = {}
        self.mem_mask = 'X' * 36

    def set_memory(self, p_index: int, p_act_num: int):
        self.add_num_masked(p_index, p_act_num)
        self.add_num_masked2(p_index, p_act_num)

    def add_num_masked(self, p_index: int, p_act_num: int):
        masked_bin = ''
        for a, b in zip(self.mem_mask, "{0:036b}".format(p_act_num)):
            if a == 'X':
                masked_bin += b
            else:
                masked_bin += a
        self.mem_dict[p_index] = int(masked_bin, 2)

    def add_num_masked2(self, p_index: int, p_act_num: int):
        x_count = self.mem_mask.count('X')
        for n in range(2 ** x_count):
            x_change = list("{0:036b}".format(n))
            masked_index = ''
            for a, b in zip(self.mem_mask, "{0:036b}".format(p_index)):
                if a == 'X':
                    masked_index += x_change.pop(-1)
                elif a == '1':
                    masked_index += '1'
                else:
                    masked_index += b
            self.mem_dict2[int(masked_index, 2)] = p_act_num


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    m = CMemory()

    for act_line in yield_input_data(p_input_file_path, p_chars_to_space='='):
        if act_line[0] == 'mask':
            m.mem_mask = act_line[1]
        else:
            m.set_memory(int(act_line[0][4:-1]), act_line[1])
    answer1 = sum([mv for mv in m.mem_dict.values()])
    answer2 = sum([mv for mv in m.mem_dict2.values()])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 14, solve_puzzle)


if __name__ == '__main__':
    main()
