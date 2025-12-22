import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


class CNode:
    def __init__(self):
        self.child_nodes: list[CNode] = list()
        self.metadata_list: list[int] = list()

    @property
    def meta_sum(self) -> int:
        return sum(self.metadata_list + [0]) + sum([cn.meta_sum for cn in self.child_nodes])

    @property
    def indexed_meta_sum(self) -> int:
        if not self.child_nodes:
            return sum(self.metadata_list + [0])
        rv = 0
        for child_to_sum in self.metadata_list:
            if child_to_sum == 0 or child_to_sum > len(self.child_nodes):
                continue
            rv += self.child_nodes[child_to_sum-1].indexed_meta_sum
        return rv


def create_node(p_input_list: list[int]) -> CNode:
    new_node = CNode()
    p_child_nodes_count = p_input_list.pop(0)
    p_metadata_count = p_input_list.pop(0)
    for _ in range(p_child_nodes_count):
        child_node = create_node(p_input_list)
        new_node.child_nodes.append(child_node)
    for _ in range(p_metadata_count):
        new_node.metadata_list.append(p_input_list.pop(0))
    return new_node


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:

    input_row = next(yield_input_data(p_input_file_path), None)

    root_node = create_node(input_row)
    answer1 = root_node.meta_sum
    answer2 = root_node.indexed_meta_sum

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 8, solve_puzzle)


if __name__ == '__main__':
    main()
