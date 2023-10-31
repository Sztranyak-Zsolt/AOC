from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_tree import CTreeNode


class CTreeHandler:
    def __init__(self):
        self.node_dict: dict[str, CTreeNode] = {}

    def get_tree_node(self, p_key: str) -> CTreeNode:
        if p_key not in self.node_dict:
            self.node_dict[p_key] = CTreeNode()
        return self.node_dict[p_key]

    @property
    def sum_all_children(self) -> int:
        return sum([tn.count_all_children for tn in self.node_dict.values()])


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer2 = None
    th = CTreeHandler()
    for orbit1, orbit2 in yield_input_data(p_input_file_path, p_chars_to_space=')'):
        th.get_tree_node(orbit1).add_child(th.get_tree_node(orbit2))
    answer1 = th.sum_all_children

    you_parents = list(th.node_dict["YOU"].yield_parents())
    for i, san_parent in enumerate(th.node_dict['SAN'].yield_parents()):
        if san_parent in you_parents:
            answer2 = i + you_parents.index(san_parent)
            break

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 6, solve_puzzle)


if __name__ == '__main__':
    main()
