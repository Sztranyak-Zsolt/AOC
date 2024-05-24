from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from math import prod
import networkx as nx


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer2 = None
    G = nx.Graph()
    for inp_row in yield_input_data(p_input_file_path,
                                    p_whole_row=False,
                                    p_chars_to_space=':'
                                    ):
        act_node = inp_row[0]
        for nn in inp_row[1:]:
            G.add_edge(act_node, nn)
    G.remove_edges_from(nx.minimum_edge_cut(G))
    answer1 = prod(len(c) for c in nx.connected_components(G))

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 25, solve_puzzle)


if __name__ == '__main__':
    main()
