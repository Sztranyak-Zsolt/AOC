from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import mh_distance, Position2D, add_positions, mul_position


class CShip:
    direction_dict = {'E': Position2D(1, 0), 'S': Position2D(0, -1), 'W': Position2D(-1, 0), 'N': Position2D(0, 1)}
    turn_dict = {'L': -1, 'R': 1}

    def __init__(self):
        self.starting_position = Position2D(0, 0)
        self.starting_direction = Position2D(1, 0)
        self.instruction_list: list[list[str, int]] = list()

    @property
    def route_end_position(self) -> Position2D:
        act_position = self.starting_position
        act_dir = self.starting_direction
        for i, v in self.instruction_list:
            if i in 'RL':
                act_dir_index = list(self.direction_dict.values()).index(act_dir)
                new_dir_index = (act_dir_index + v * self.turn_dict[i] // 90) % 4
                act_dir = list(self.direction_dict.values())[new_dir_index]
                continue
            if i in 'ESWN':
                dir_to_use = self.direction_dict[i]
            else:
                dir_to_use = act_dir
            act_position = add_positions(act_position, mul_position(dir_to_use, v))
        return act_position

    @property
    def route_end_position2(self) -> tuple[int, int]:
        act_position = self.starting_position
        act_wp = Position2D(10, 1)
        for i, v in self.instruction_list:
            if i == 'F':
                act_position = add_positions(act_position, mul_position(act_wp, v))
            elif i in 'ESWN':
                act_wp = add_positions(act_wp, mul_position(self.direction_dict[i], v))
            elif i in 'RL':
                if (self.turn_dict[i] * v // 90) % 4 == 1:
                    act_wp = Position2D(act_wp.y, -act_wp.x)
                elif (self.turn_dict[i] * v // 90) % 4 == 2:
                    act_wp = Position2D(-act_wp.x, -act_wp.y)
                elif (self.turn_dict[i] * v // 90) % 4 == 3:
                    act_wp = Position2D(-act_wp.y, act_wp.x)
        return act_position

    @property
    def mh_distance_route1(self) -> int:
        return mh_distance(self.starting_position, self.route_end_position)

    @property
    def mh_distance_route2(self) -> int:
        return mh_distance(self.starting_position, self.route_end_position2)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    s = CShip()
    for act_line in yield_input_data(p_input_file_path, p_whole_row=True):
        s.instruction_list.append([act_line[0], int(act_line[1:])])

    answer1 = s.mh_distance_route1
    answer2 = s.mh_distance_route2

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 12, solve_puzzle)


if __name__ == '__main__':
    main()
