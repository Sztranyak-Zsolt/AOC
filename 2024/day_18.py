from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, neighbor_positions


class CMaze(CGridBase):
    def __init__(self):
        super().__init__()
        self.max_x = 70
        self.max_y = 70

    def find_route(self):
        start_position = Position2D(0, 0)
        target_position = Position2D(self.max_x, self.max_y)
        act_step = 0
        act_pos_list = [start_position]
        visited = {start_position, }
        while act_pos_list:
            next_pos_list = []
            act_step += 1
            for act_pos in act_pos_list:
                for next_pos in neighbor_positions(act_pos, p_return_corner=False):
                    if next_pos.x in (-1, self.max_x + 1) or next_pos.y in (-1, self.max_y + 1) or next_pos in visited \
                            or next_pos in self.position_dict:
                        continue
                    if next_pos == target_position:
                        return act_step
                    visited.add(next_pos)
                    next_pos_list.append(next_pos)
            act_pos_list = next_pos_list


def find_first_non_valid_position(p_wall_coordinates: list[Position2D]) -> Position2D:
    m = CMaze()
    act_min_step = 0
    act_max_step = len(p_wall_coordinates) - 1
    while act_min_step != act_max_step:
        act_mid_step = (act_min_step + act_max_step) // 2
        m.position_dict.clear()
        for act_pos in p_wall_coordinates[:act_mid_step+1]:
            m.add_item(act_pos, '#')
        if m.find_route() is None:
            act_max_step = act_mid_step
        else:
            act_min_step = act_mid_step + 1
    return p_wall_coordinates[act_min_step]


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    coordinates: list[Position2D] = []
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space=','):
        coordinates.append(Position2D(*inp_row))

    m = CMaze()
    for act_pos in coordinates[:1024]:
        m.add_item(act_pos, p_item='#')
    answer1 = m.find_route()

    answer2 = ','.join([str(p) for p in find_first_non_valid_position(coordinates)])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 18, solve_puzzle)


if __name__ == '__main__':
    main()
