from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_graph import CGraphItem


class CGraphItemHandler:
    def __init__(self):
        self.graph_list: dict[int, CGraphItem] = {}

    def get_graph_item(self, p_key: int) -> CGraphItem:
        if p_key not in self.graph_list:
            self.graph_list[p_key] = CGraphItem(p_key)
        return self.graph_list[p_key]

    @property
    def graph_group_count(self):
        return len(set([g.get_group_head() for g in self.graph_list.values()]))

    def get_group_members_count(self, p_key) -> int:
        graph0_head = self.graph_list[p_key].get_group_head()
        return len([g for g in self.graph_list.values() if g.get_group_head() == graph0_head])


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    nh = CGraphItemHandler()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='<->,'):
        act_node = nh.get_graph_item(inp_row[0])
        for connected_node in inp_row[1:]:
            if connected_node != inp_row[0]:
                act_node.connect_node(nh.get_graph_item(connected_node))

    answer1 = nh.get_group_members_count(0)
    answer2 = nh.graph_group_count

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 12, solve_puzzle)


if __name__ == '__main__':
    main()
