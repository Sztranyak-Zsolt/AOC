from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from math import lcm


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    node_dict = {}
    act_nodes = []
    nodes_cycle_time = {}
    input_iterator = iter(yield_input_data(p_input_file_path, p_chars_to_space='(,=)', p_group_separator='\n\n'))
    step_directions = next(input_iterator)[0][0]
    for orig_node, left_node, right_node in next(input_iterator):
        node_dict[orig_node] = (left_node, right_node)
        if orig_node[-1] == 'A':
            act_nodes.append([orig_node, orig_node])

    # as starting nodes next directions are equals end nodes next directions, movements are periodic
    c = 0
    while act_nodes:
        next_int = step_directions[c % len(step_directions)]
        c += 1
        n = 0 if next_int == 'L' else 1
        next_nodes = []
        for act_node, starting_node in act_nodes:
            next_node = node_dict[act_node][n]
            if next_node[-1] == 'Z':
                nodes_cycle_time[starting_node] = c
                continue
            next_nodes.append([next_node, starting_node])
        act_nodes = next_nodes

    answer1 = nodes_cycle_time['AAA']
    answer2 = lcm(*nodes_cycle_time.values())

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 8, solve_puzzle)


if __name__ == '__main__':
    main()
