from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_tree import CTreeNode
from typing import Self


class CGarbage(CTreeNode):
    def __init__(self):
        super().__init__()
        self.parent_item: Self | None = None
        self.child_list: list[Self] = list()
        self.garbage_list: list[str] = list()

    def add_garbage(self, p_garbage_string: str) -> str:
        if p_garbage_string[0] != "<":
            return p_garbage_string
        p_garbage_string = p_garbage_string[1:]
        self.garbage_list.append('')
        to_escape = False
        while p_garbage_string:
            act_char = p_garbage_string[0]
            if to_escape:
                to_escape = False
            elif act_char == '!':
                to_escape = True
            elif act_char == ">":
                return p_garbage_string[1:]
            else:
                self.garbage_list[-1] += act_char
            p_garbage_string = p_garbage_string[1:]
        return ''

    def create_garbage_pack(self, p_garbage_string: str) -> str:
        if p_garbage_string[0] != '{':
            return p_garbage_string
        p_garbage_string = p_garbage_string[1:]
        while p_garbage_string:
            act_char = p_garbage_string[0]
            if act_char == "<":
                p_garbage_string = self.add_garbage(p_garbage_string)
                continue
            elif act_char == "{":
                new_garbage = CGarbage()
                self.add_child(new_garbage)
                p_garbage_string = new_garbage.create_garbage_pack(p_garbage_string)
                continue
            elif act_char == "}":
                return p_garbage_string[1:]
            p_garbage_string = p_garbage_string[1:]

    def sum_level(self):
        return self.act_level + sum([x.sum_level() for x in self.child_list])

    def sum_string(self):
        return sum([len(x) for x in self.garbage_list]) + sum([x.sum_string() for x in self.child_list])


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    gs = next(yield_input_data(p_input_file_path, p_whole_row=True), None)

    g = CGarbage()
    g.create_garbage_pack(gs)

    answer1 = g.sum_level()
    answer2 = g.sum_string()

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 9, solve_puzzle)


if __name__ == '__main__':
    main()
