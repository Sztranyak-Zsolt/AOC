from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CDistressedSignal:
    def __init__(self, p_signal: list):
        self.signal_list = []
        for child_signal in p_signal:
            if isinstance(child_signal, int):
                self.signal_list.append(child_signal)
            else:
                self.signal_list.append(CDistressedSignal(child_signal))

    def __str__(self):
        return '[' + ','.join([str(x) for x in self.signal_list]) + ']'

    def __gt__(self, other):
        if isinstance(other, int):
            return CDistressedSignal([other]) < self
        if not self.signal_list:
            return False
        if not other.signal_list:
            return True
        for cd1, cd2 in zip(self.signal_list, other.signal_list):
            if isinstance(cd1, int) and not isinstance(cd2, int):
                cd1 = CDistressedSignal([cd1])
            elif isinstance(cd2, int) and not isinstance(cd1, int):
                cd2 = CDistressedSignal([cd2])
            if cd1 < cd2:
                return False
            elif cd2 < cd1:
                return True
        return len(other.signal_list) < len(self.signal_list)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = 0
    signal_list = []
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        if inp_row == '':
            if signal_list[-2] < signal_list[-1]:
                answer1 += len(signal_list) // 2
            continue
        signal_list.append(CDistressedSignal(eval(inp_row)))
    if signal_list[-2] < signal_list[-1]:
        answer1 += len(signal_list) // 2

    s2 = CDistressedSignal([[2]])
    s6 = CDistressedSignal([[6]])
    signal_list.extend([s2, s6])
    signal_list.sort()
    answer2 = (signal_list.index(s2) + 1) * (signal_list.index(s6) + 1)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 13, solve_puzzle)


if __name__ == '__main__':
    main()
