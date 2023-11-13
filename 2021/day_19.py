from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_space import CSpaceBase, CVector3D, TP3D
from copy import copy


class CScanner(CSpaceBase):
    def __init__(self):
        super().__init__()
        self.difference_set = set()
        self.point_vector_dict: dict[CVector3D, set[CVector3D]] = {}

    def add_item(self, p_position: CVector3D, act_value: str = '#'):
        self.point_vector_dict[p_position] = set()
        for prev_position in self.position_dict:
            self.difference_set.add(int(p_position - prev_position))
            self.point_vector_dict[p_position].add(p_position - prev_position)
            self.point_vector_dict[prev_position].add(prev_position - p_position)
        super().add_item(p_position, '#')

    def set_point_difs(self):
        for act_point in self.position_dict:
            if act_point not in self.point_vector_dict:
                self.point_vector_dict[act_point] = set()
            for next_point in self.position_dict:
                if act_point == next_point:
                    continue
                if next_point not in self.point_vector_dict:
                    self.point_vector_dict[next_point] = set()
                self.difference_set.add(int(act_point - next_point))
                self.point_vector_dict[act_point].add(next_point)
                self.point_vector_dict[next_point].add(act_point)

    def set_other_orientations(self):
        super().set_other_orientations()
        for act_orientation in self.other_orientations.values():
            if id(act_orientation) != id(self):
                act_orientation.set_point_difs()

    def offset_space(self, p_vector: TP3D):
        os = super().offset_space(p_vector)
        os.set_point_difs()
        return os


class CScannerHandler:
    def __init__(self):
        self.scanner_list: list[CScanner] = []

    def build_space(self):
        base_space = copy(self.scanner_list[0])
        base_scanner_position = CVector3D(0, 0, 0)
        base_space.scanner_positions = {base_scanner_position}
        base_space.difference_set = self.scanner_list[0].difference_set.copy()
        base_space.point_vector_dict = self.scanner_list[0].point_vector_dict.copy()
        known_scanners = {self.scanner_list[0]}
        new_scanner_found = True
        while new_scanner_found:
            new_scanner_found = False
            for act_scanner in self.scanner_list:
                if act_scanner in known_scanners or len(base_space.difference_set & act_scanner.difference_set) < 10:
                    continue
                if not act_scanner.other_orientations:
                    act_scanner.set_other_orientations()
                for act_scanner_orientation_space in act_scanner.other_orientations.values():
                    for act_point, act_point_dif_set in act_scanner_orientation_space.point_vector_dict.items():
                        for base_point, base_point_dif_set in base_space.point_vector_dict.items():
                            if len(act_point_dif_set & base_point_dif_set) < 10:
                                continue
                            new_scanner_found = True
                            new_scanner_position = base_point - act_point
                            base_space.scanner_positions.add(new_scanner_position)
                            space_to_be_added = act_scanner_orientation_space.offset_space(new_scanner_position)
                            known_scanners.add(act_scanner)
                            base_space.difference_set |= space_to_be_added.difference_set
                            for act_position in space_to_be_added.position_dict:
                                if act_position not in base_space.position_dict:
                                    base_space.add_item(act_position)
                                    base_space.point_vector_dict[act_position] = space_to_be_added.point_vector_dict[act_position]
                                else:
                                    base_space.point_vector_dict[act_position] |= space_to_be_added.point_vector_dict[act_position]
                            break
        return base_space


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer2 = 0
    sh = CScannerHandler()
    for inp_group in yield_input_data(p_input_file_path, p_group_separator='\n\n', p_chars_to_space=','):
        for inp_row in inp_group:
            if len(inp_row) == 4:
                sh.scanner_list.append(CScanner())
            else:
                sh.scanner_list[-1].add_item(CVector3D(*inp_row))
    whole_space = sh.build_space()
    answer1 = len(whole_space.position_dict)
    for s1 in whole_space.scanner_positions:
        for s2 in whole_space.scanner_positions:
            answer2 = max(answer2, int(s1 - s2))
    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 19, solve_puzzle)


if __name__ == '__main__':
    main()
