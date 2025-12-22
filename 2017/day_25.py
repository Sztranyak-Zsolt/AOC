import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from collections import defaultdict


class CState:
    def __init__(self, p_id: str):
        self.id = p_id
        self.write: dict[bool, bool] = dict()
        self.move: dict[bool, int] = dict()
        self.next_state: dict[bool, CState] = dict()


class CStateHandler:
    def __init__(self):
        self.state_dict: dict[str, CState] = {}
        self.act_state: CState | None = None
        self.act_cursor = 0
        self.tape: defaultdict[int, bool] = defaultdict(lambda: False)

    def get_state(self, p_state_id: str):
        if p_state_id not in self.state_dict:
            self.state_dict[p_state_id] = CState(p_state_id)
        return self.state_dict[p_state_id]

    def run_diagnostic(self, p_step: int):
        for _ in range(p_step):
            act_tape_value = self.tape[self.act_cursor]
            self.tape[self.act_cursor] = self.act_state.write[act_tape_value]
            self.act_cursor += self.act_state.move[act_tape_value]
            self.act_state = self.act_state.next_state[act_tape_value]


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    checksum_step = 0
    sh = CStateHandler()
    for i, inp_row in enumerate(yield_input_data(p_input_file_path, p_group_separator='\n\n', p_chars_to_space='.:')):
        if i == 0:
            sh.act_state = sh.get_state(inp_row[0][-1])
            checksum_step = inp_row[1][-2]
        else:
            act_state = sh.get_state(inp_row[0][-1])
            act_state.write = {False: inp_row[2][-1] == 1,
                               True: inp_row[6][-1] == 1}
            act_state.move = {False: 1 if inp_row[3][-1] == 'right' else -1,
                              True: 1 if inp_row[7][-1] == 'right' else -1}
            act_state.next_state = {False: sh.get_state(inp_row[4][-1]),
                                    True: sh.get_state(inp_row[8][-1])}
    sh.run_diagnostic(checksum_step)
    answer1 = sum(sh.tape.values())

    return answer1, None


def main():
    aoc_solve_puzzle(2017, 25, solve_puzzle)


if __name__ == '__main__':
    main()
