from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class COutput:
    def __init__(self, p_id: int):
        self.id = p_id
        self.chip_values: list[int] = []


class CRobot:
    def __init__(self, p_id: int):
        self.id = p_id
        self.starting_values: list[int] = []
        self.chip_values: list[int] = []
        self.give_chips_to: dict[bool: CRobot | COutput] = {}


class CFactory:
    def __init__(self):
        self.robot_dict: dict[int, CRobot] = {}
        self.output_dict: dict[int, COutput] = {}

    def get_robot(self, p_id: int) -> CRobot:
        if p_id not in self.robot_dict:
            self.robot_dict[p_id] = CRobot(p_id)
        return self.robot_dict[p_id]

    def get_output(self, p_id: int) -> COutput:
        if p_id not in self.output_dict:
            self.output_dict[p_id] = COutput(p_id)
        return self.output_dict[p_id]

    def add_robot_instruction(self, p_robot_id: int, p_is_high: bool, p_output_type: str, p_output_id: int):
        if p_output_type == 'bot':
            self.get_robot(p_robot_id).give_chips_to[p_is_high] = self.get_robot(p_output_id)
        else:
            self.get_robot(p_robot_id).give_chips_to[p_is_high] = self.get_output(p_output_id)

    def produce(self) -> int:
        rv17_61 = None
        for r in self.robot_dict.values():
            r.chip_values = r.starting_values.copy()
        robot_found = True
        while robot_found:
            robot_found = False
            for r in self.robot_dict.values():
                if len(r.chip_values) == 2:
                    robot_found = True
                    if rv17_61 is None and sorted(r.chip_values) == [17, 61]:
                        rv17_61 = r.id
                    r.give_chips_to[False].chip_values.append(min(r.chip_values))
                    r.give_chips_to[True].chip_values.append(max(r.chip_values))
                    r.chip_values = []
        return rv17_61


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    f = CFactory()
    for inp_row in yield_input_data(p_input_file_path):
        if inp_row[0] == 'value':
            f.get_robot(inp_row[5]).starting_values.append(inp_row[1])
            continue
        f.add_robot_instruction(inp_row[1], False, inp_row[5], inp_row[6])
        f.add_robot_instruction(inp_row[1], True, inp_row[10], inp_row[11])

    answer1 = f.produce()
    answer2 = f.output_dict[0].chip_values[0] * f.output_dict[1].chip_values[0] * f.output_dict[2].chip_values[0]

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 10, solve_puzzle)


if __name__ == '__main__':
    main()
