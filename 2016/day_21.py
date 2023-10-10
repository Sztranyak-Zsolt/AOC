from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def swap_position(p_string_list: list[str], p1: int, p2: int):
    s1 = p_string_list[p1]
    p_string_list[p1] = p_string_list[p2]
    p_string_list[p2] = s1


def rotate_left(p_string_list: list[str], p_step: int, p_reverse: bool = False):
    if p_reverse:
        p_step = -p_step
    p_st_corr = p_step % len(p_string_list)
    first_part = p_string_list[:p_st_corr]
    del p_string_list[:p_st_corr]
    p_string_list += first_part


def rotate_right(p_string_list: list[str], p_step: int, p_reverse: bool = False):
    rotate_left(p_string_list, -p_step, p_reverse)


def swap_letter(p_string_list: list[str], ps1: str, ps2: str):
    p1 = p_string_list.index(ps1)
    p2 = p_string_list.index(ps2)
    swap_position(p_string_list, p1, p2)


def rotate_based(p_string_list: list[str], ps1: str, p_reverse: bool = False):
    p1 = p_string_list.index(ps1)
    if not p_reverse:
        if p1 >= 4:
            rotate_left(p_string_list, -p1 - 2)
        else:
            rotate_left(p_string_list, -p1 - 1)
    else:
        if p1 % 2 == 1:
            rotate_left(p_string_list, p1 // 2 + 1)
        else:
            if p1 == 2:
                rotate_left(p_string_list, -2)
            if p1 == 4:
                rotate_left(p_string_list, -1)
            if p1 == 6:
                rotate_left(p_string_list, 0)
            if p1 == 0:
                rotate_left(p_string_list, 1)


def reverse_position(p_string_list: list[str], p1: int, p2: int):
    first_part = p_string_list[:p1]
    second_part = p_string_list[p1:p2+1][::-1]
    last_part = p_string_list[p2+1:]
    del p_string_list[::]
    p_string_list += first_part + second_part + last_part


def move_position(p_string_list: list[str], p1: int, p2: int, p_reverse: bool = False):
    if p_reverse:
        move_position(p_string_list, p2, p1)
    else:
        st = p_string_list.pop(p1)
        p_string_list.insert(p2, st)


class CScramble:
    def __init__(self, p_str: str, p_reverse: bool = False):
        self.starting_string = list(p_str)
        self.instruction_list = list()
        self.reverse = p_reverse

    @property
    def linked_string(self):
        act_string = self.starting_string.copy()
        if self.reverse:
            sl = slice(None, None, -1)
        else:
            sl = slice(None, None, None)
        for act_instruction in self.instruction_list[sl]:
            print(act_instruction)
            act_instruction[0](act_string, *act_instruction[1])
        return ''.join(act_string)

    def add_raw_instruction(self, p_instruction_row: list):
        if p_instruction_row[0] == 'swap':
            if p_instruction_row[1] == 'position':
                self.instruction_list.append((swap_position, (p_instruction_row[2], p_instruction_row[5])))
            elif p_instruction_row[1] == 'letter':
                self.instruction_list.append((swap_letter, (p_instruction_row[2], p_instruction_row[5])))
        elif p_instruction_row[0] == 'rotate':
            if p_instruction_row[1] == 'left':
                self.instruction_list.append((rotate_left, tuple([p_instruction_row[2], self.reverse])))
            elif p_instruction_row[1] == 'right':
                self.instruction_list.append((rotate_right, tuple([p_instruction_row[2], self.reverse])))
            elif p_instruction_row[1] == 'based':
                self.instruction_list.append((rotate_based, tuple([p_instruction_row[6], self.reverse])))
        elif p_instruction_row[0] == 'reverse':
            self.instruction_list.append((reverse_position, (p_instruction_row[2], p_instruction_row[4])))
        elif p_instruction_row[0] == 'move':
            self.instruction_list.append((move_position, (p_instruction_row[2], p_instruction_row[5], self.reverse)))


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    s1 = CScramble('abcdefgh')
    s2 = CScramble('fbgdceah', True)
    for inp_row in yield_input_data(p_input_file_path):
        s1.add_raw_instruction(inp_row)
        s2.add_raw_instruction(inp_row)

    answer1 = s1.linked_string
    answer2 = s2.linked_string

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 21, solve_puzzle)


if __name__ == '__main__':
    main()
