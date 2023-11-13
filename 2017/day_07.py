from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_tree import CTreeHandler
from collections import defaultdict


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    th = CTreeHandler()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='(),->'):
        th.get_tree_node(inp_row[0]).value = inp_row[1]
        for child_node in inp_row[2:]:
            th.get_tree_node(inp_row[0]).add_child(th.get_tree_node(child_node))

    root_item = list(th.node_dict.values())[0].root_node
    answer1 = root_item.name
    unbalanced_item = root_item

    while not unbalanced_item.is_value_balanced:
        for child_item in unbalanced_item.child_list:
            if not child_item.is_value_balanced:
                unbalanced_item = child_item
                break
        else:
            break

    w_dict = defaultdict(lambda: [])
    for act_ch in unbalanced_item.child_list:
        w_dict[act_ch.sum_values].append(act_ch)
    anomaly_disk_value = [v[0].value for v in w_dict.values() if len(v) == 1][0]
    anomaly_sum_value = [v[0].sum_values for v in w_dict.values() if len(v) == 1][0]
    normal_sum_value = [v[0].sum_values for v in w_dict.values() if len(v) != 1][0]

    answer2 = anomaly_disk_value - (anomaly_sum_value - normal_sum_value)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 7, solve_puzzle)


if __name__ == '__main__':
    main()
