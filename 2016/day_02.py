from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import add_positions


direction = {"U": [-1, 0], "R": [0, 1], "D": [1, 0], "L": [0, -1]}


class CKeypad:
    def __init__(self, p_keypad: list[list[str | None]], p_act_position_char: str):
        self.keypad: dict[(int, int), str] = {}
        self.position = (0, 0)
        for rn, keypad_row in enumerate(p_keypad):
            for cn, keypad_char in enumerate(keypad_row):
                if keypad_char is None:
                    continue
                self.keypad[(rn, cn)] = keypad_char
                if keypad_char == p_act_position_char:
                    self.position = (rn, cn)

    @property
    def act_number(self) -> str:
        return self.keypad[self.position]

    def goto_direction(self, p_direction: str):
        new_pos = add_positions(self.position, direction[p_direction])
        if new_pos in self.keypad:
            self.position = new_pos


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = ''
    kp = CKeypad([['1', '2', '3'],
                  ['4', '5', '6'],
                  ['7', '8', '9']], '5')
    kp2 = CKeypad([[None, None, None, "1"],
                   [None, None, "2", "3", "4"],
                   [None, "5", "6", "7", "8", "9"],
                   [None, None, "A", "B", "C"],
                   [None, None, None, "D"]], '7')
    for direction_row in yield_input_data(p_input_file_path, p_whole_row=True):
        for act_dir in direction_row:
            kp.goto_direction(act_dir)
            kp2.goto_direction(act_dir)
        answer1 += kp.act_number
        answer2 += kp2.act_number

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 2, solve_puzzle)


if __name__ == '__main__':
    main()
