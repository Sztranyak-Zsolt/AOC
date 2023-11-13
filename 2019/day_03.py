from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import CVector2D


class CWire:
    def __init__(self):
        self.position_dict: dict[CVector2D, int] = {}

    def create_wire_from_raw(self, p_raw_dir: list[str]):
        dir_dict = {'R': CVector2D(-1, 0), 'L': CVector2D(1, 0), 'U': CVector2D(0, 1), 'D': CVector2D(0, -1)}
        act_position = CVector2D(0, 0)
        step_counter = 0
        for act_step in p_raw_dir:
            act_dir = dir_dict[act_step[0]]
            for step in range(1, int(act_step[1:]) + 1):
                step_counter += 1
                act_position = act_position + act_dir
                if act_position not in self.position_dict:
                    self.position_dict[act_position] = step_counter


def wire_crosses(p_wire1: CWire, p_wire2: CWire) -> dict[CVector2D, int]:
    rd = {}
    for other_pos, other_step in p_wire2.position_dict.items():
        if other_pos in p_wire1.position_dict:
            rd[other_pos] = other_step + p_wire1.position_dict[other_pos]
    return rd


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    wire1 = CWire()
    wire2 = CWire()
    for i, inp_row in enumerate(yield_input_data(p_input_file_path, p_chars_to_space=',')):
        if i == 0:
            wire1.create_wire_from_raw(inp_row)
        else:
            wire2.create_wire_from_raw(inp_row)
    crosses = wire_crosses(wire1, wire2)
    answer1 = min([int(p) for p in crosses])
    answer2 = min(crosses.values())

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 3, solve_puzzle)


if __name__ == '__main__':
    main()
