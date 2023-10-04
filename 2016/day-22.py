from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase, CBaseItem, neighbor_positions
from collections import deque


class CNode(CBaseItem):
    def __init__(self, p_value: str, p_size: int, p_used: int, p_avail: int, p_used_perc: int):
        super().__init__(p_value)
        self.size = p_size
        self.used = p_used
        self.avail = p_avail
        self.used_perc = p_used_perc


class CNodeManager(CGridBase):
    def __init__(self):
        super().__init__()
        self.position_dict: dict[tuple[int, int], CNode] = {}

    @property
    def viable_nodes_count(self) -> int:
        rv = 0
        for n1 in self.position_dict.values():
            for n2 in self.position_dict.values():
                if n1 != n2 and n1.used <= n2.avail and n1.used != 0:
                    rv += 1
        return rv

    @property
    def empty_node_position(self) -> tuple[int, int]:
        for k, v in self.position_dict.items():
            if v.used == 0:
                return k

    def step_to_target(self, p_starting_position: tuple[int, int], p_target_position: tuple[int, int]) -> int:
        known_positions = {p_starting_position}
        dq = deque([[p_starting_position, 0]])
        while dq:
            act_position, act_step = dq.popleft()
            for next_x, next_y in neighbor_positions(act_position):
                if (next_x, next_y) not in known_positions:
                    known_positions.add((next_x, next_y))
                    if (next_x, next_y) == p_target_position:
                        return act_step + 1
                    try:
                        if self.position_dict[(next_x, next_y)].used < 85:
                            dq.append([(next_x, next_y), act_step + 1])
                    except KeyError:
                        continue
        return -1

    def __str__(self):
        ret_str = list()
        for y in range(self.max_y + 1):
            row_str = list()
            for x in range(self.max_x + 1):
                if (x, y) in self.position_dict:
                    row_str.append(str(self.position_dict[(x, y)].used))
                else:
                    row_str.append('    ')
            ret_str.append('|'.join(row_str))
        return '\n'.join(ret_str)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    nm = CNodeManager()
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='T%xy-'):
        if inp_row[0][:4] in ('root', 'File'):
            continue
        _, x, y, size, used, avail, use_perc = inp_row
        nm.add_item((x, y), CNode(f'x{x}y{y}', size, used, avail, use_perc))

    answer1 = nm.viable_nodes_count
    answer2 = nm.step_to_target(nm.empty_node_position, (nm.max_x, 0)) \
        + (nm.step_to_target((0, 0), (nm.max_x, 0)) - 1) * 5

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 22, solve_puzzle)


if __name__ == '__main__':
    main()
