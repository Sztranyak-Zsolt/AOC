from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_tree import CTreeNode


class CItem(CTreeNode):
    def __init__(self, p_name: str, p_folder: bool, p_value: int = 0):
        super().__init__(p_name, p_value)
        self.is_folder = p_folder
        self.ls: dict[str: CItem] = dict()
        self.parent: CItem | None = None

    @property
    def folder_size(self) -> int:
        if not self.ls:
            return self.value
        return sum([i.folder_size for i in self.ls.values()])

    def yield_all_folder(self):
        for ln in self.ls.values():
            for lni in ln.yield_all_folder():
                if lni.is_folder:
                    yield lni
        if self.is_folder:
            yield self


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    root = act_item = CItem('/', True)
    for command_list in yield_input_data(p_input_file_path):
        if command_list[0] == "$":
            if command_list[1] == "ls":
                continue
            if command_list[2] == "/":
                act_item = act_item.root_node
            elif command_list[2] == "..":
                act_item = act_item.parent_item
            else:
                act_item = act_item.ls[command_list[2]]
        elif command_list[0] == "dir":
            if command_list[1] not in act_item.ls:
                new_folder = CItem(command_list[1], True)
                new_folder.parent_item = act_item
                act_item.ls[command_list[1]] = new_folder
        elif command_list[1] not in act_item.ls:
            new_item = CItem(command_list[1], False, command_list[0])
            act_item.ls[command_list[1]] = new_item
    answer1 = sum([x.folder_size for x in root.yield_all_folder() if x.folder_size <= 100000])
    to_clean = root.folder_size - 40000000
    answer2 = min([x.folder_size for x in root.yield_all_folder() if x.folder_size > to_clean])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 7, solve_puzzle)


if __name__ == '__main__':
    main()
