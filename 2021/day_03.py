from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CSignalList:
    def __init__(self):
        self.signal_list = list()

    def calc_gamma_rate(self):
        s_dict = {i: 0 for i in range(12)}
        for signal in self.signal_list:
            for i, letter in enumerate(signal):
                s_dict[i] += int(letter)
        return int(''.join(['1' if x > len(self.signal_list) // 2 else '0' for x in s_dict.values()]), 2)

    def calc_epsilon_rate(self):
        s_dict = {i: 0 for i in range(12)}
        for signal in self.signal_list:
            for i, letter in enumerate(signal):
                s_dict[i] += int(letter)
        return int(''.join(['0' if x > len(self.signal_list) // 2 else '1' for x in s_dict.values()]), 2)

    def calc_o2_rating(self):
        act_list = self.signal_list.copy()
        for act_index in range(12):
            mc_value = '1' if len(['x' for s in act_list if s[act_index] == '1']) * 2 >= len(act_list) else '0'
            act_list = [s for s in act_list if s[act_index] == mc_value]
            if len(act_list) == 1:
                break
        return int(act_list[0], 2)

    def calc_co2_rating(self):
        act_list = self.signal_list.copy()
        for act_index in range(12):
            lc_value = '0' if len(['x' for s in act_list if s[act_index] == '1']) * 2 >= len(act_list) else '1'
            act_list = [s for s in act_list if s[act_index] == lc_value]
            if len(act_list) == 1:
                break
        return int(act_list[0], 2)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    s = CSignalList()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False):
        s.signal_list.append(inp_row)
    answer1 = s.calc_epsilon_rate() * s.calc_gamma_rate()
    answer2 = s.calc_o2_rating() * s.calc_co2_rating()
    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 3, solve_puzzle)


if __name__ == '__main__':
    main()
