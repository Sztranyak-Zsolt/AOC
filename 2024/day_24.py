import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from operator import and_, or_, xor
from typing import Callable


class CCalculator:
    def __init__(self):
        self.node_dict: dict[str, bool] = {}
        self.node_calcs: dict[str, list[Callable, str, str]] = {}

    @property
    def x(self) -> int:
        return self.get_value('x')

    @x.setter
    def x(self, p_value: int):
        self.set_value('x', p_value)

    @property
    def y(self) -> int:
        return self.get_value('y')

    @y.setter
    def y(self, p_value: int):
        self.set_value('y', p_value)

    @property
    def z(self) -> int:
        self.calculate()
        return self.get_value('z')

    def get_value(self, p_c: str) -> int | None:
        if p_c not in ('x', 'y', 'z'):
            return None
        p = 0
        rv = 0
        while f'{p_c}{p:02}' in self.node_dict:
            if self.node_dict[f'{p_c}{p:02}']:
                rv += (1 << p)
            p += 1
        return rv

    def set_value(self, p_c: str, p_value: int):
        if p_c not in ('x', 'y'):
            return
        for node_code, node_val in self.node_dict.items():
            if node_val and node_code[0] == p_c:
                self.node_dict[node_code] = False
        p = 0
        while p_value:
            if p_value & 1:
                self.node_dict[f'{p_c}{p:02}'] = True
            p += 1
            p_value >>= 1

    def calculate(self):
        known_nodes = {n for n in self.node_dict if n[0] in ('x', 'y')}
        new_calc_found = True
        while new_calc_found:
            new_calc_found = False
            for next_node, (node_op, source_node1, source_node2) in self.node_calcs.items():
                if next_node not in known_nodes and source_node1 in known_nodes and source_node2 in known_nodes:
                    self.node_dict[next_node] = node_op(self.node_dict[source_node1], self.node_dict[source_node2])
                    known_nodes.add(next_node)
                    new_calc_found = True

    def get_triggered_nodes(self, p_known_nodes: set[str]) -> set[str]:
        triggered_found = True
        all_nodes = p_known_nodes.copy()
        while triggered_found:
            triggered_found = False
            for next_node, (node_op, source_node1, source_node2) in self.node_calcs.items():
                if next_node not in all_nodes and source_node1 in all_nodes and source_node2 in all_nodes:
                    all_nodes.add(next_node)
                    triggered_found = True
        return all_nodes - p_known_nodes

    def test_addition(self, p_bit: int) -> bool:
        for x_val in range(8):
            if p_bit == 0:
                if x_val > 3:
                    continue
            for y_val in range(8):
                if p_bit == 0:
                    if y_val > 3:
                        continue
                    self.x = x_val
                    self.y = y_val
                else:
                    self.x = x_val << (p_bit - 1)
                    self.y = y_val << (p_bit - 1)
                if self.x + self.y != self.z:
                    return False
        return True

    def repair_code(self):
        proper_nodes = set()
        p = 0
        changed_nodes: list[str] = []
        while f'x{p:02}' in self.node_dict:
            proper_nodes.add(f'x{p:02}')
            proper_nodes.add(f'y{p:02}')
            triggered_nodes = self.get_triggered_nodes(proper_nodes)
            if not self.test_addition(p):
                for tr_node in triggered_nodes:
                    for change_node in self.node_calcs:
                        if change_node in proper_nodes or change_node == tr_node:
                            continue
                        self.node_calcs[tr_node], self.node_calcs[change_node] = \
                            self.node_calcs[change_node], self.node_calcs[tr_node]
                        if self.test_addition(p):
                            changed_nodes.extend([tr_node, change_node])
                            break
                        self.node_calcs[tr_node], self.node_calcs[change_node] = \
                            self.node_calcs[change_node], self.node_calcs[tr_node]
                    else:
                        continue
                    break
            proper_nodes |= self.get_triggered_nodes(proper_nodes)
            p += 1
        return changed_nodes


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    c = CCalculator()
    op_dict = {'OR': or_, 'AND': and_, 'XOR': xor}
    inp_group = iter(yield_input_data(p_input_file_path, p_chars_to_space=':->', p_group_separator='\n\n'))

    for node, node_value in next(inp_group):
        c.node_dict[node] = (node_value == 1)

    for source_node1, node_operation, source_node2, target_node in next(inp_group):
        c.node_calcs[target_node] = [op_dict[node_operation], source_node1, source_node2]

    answer1 = c.z
    answer2 = ','.join(sorted(c.repair_code()))

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 24, solve_puzzle)


if __name__ == '__main__':
    main()
