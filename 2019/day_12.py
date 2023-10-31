from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_space import CSpaceBase, Position3D
from GENERICS.aoc_grid import add_positions, mh_distance
from math import lcm


def sign(p_num: int) -> int:
    if p_num == 0:
        return 0
    if p_num > 0:
        return 1
    return -1


class CSpace(CSpaceBase):
    def __init__(self):
        super().__init__()
        self.velocity: dict[int, Position3D] = {}

    def add_item(self, p_position: Position3D, p_moon_index: int,
                 set_border_on_init: bool = False):
        super().add_item(p_position, p_moon_index, set_border_on_init)
        self.velocity[p_moon_index] = Position3D(0, 0, 0)

    def recalc_velocity(self):
        for act_moon, act_moon_index in self.position_dict.items():
            for next_moon in self.position_dict:
                vel_difi = Position3D(sign(next_moon.x - act_moon.x), sign(next_moon.y - act_moon.y),
                                      sign(next_moon.z - act_moon.z))
                self.velocity[act_moon_index] = add_positions(self.velocity[act_moon_index], vel_difi)

    def move_moons(self):
        self.recalc_velocity()
        new_position_dict = {}
        for act_moon_pos, act_moon_index in self.position_dict.items():
            new_position_dict[add_positions(act_moon_pos, self.velocity[act_moon_index])] = act_moon_index
        self.position_dict = new_position_dict

    @property
    def act_energy(self) -> int:
        rv = 0
        for act_moon, act_moon_index in self.position_dict.items():
            pot = mh_distance(act_moon, Position3D(0, 0, 0))
            kin = mh_distance(self.velocity[act_moon_index], Position3D(0, 0, 0))
            rv += pot * kin
        return rv

    def act_vector_by_axis(self, p_axis: int) -> list[int]:
        rv = list()
        for act_moon, act_moon_index in self.position_dict.items():
            rv.extend([act_moon[p_axis], self.velocity[act_moon_index][p_axis]])
        return rv

    @property
    def period_time(self) -> int:
        x_vectors_init = self.act_vector_by_axis(0)
        y_vectors_init = self.act_vector_by_axis(1)
        z_vectors_init = self.act_vector_by_axis(2)
        x_vector_period = y_vector_period = z_vector_period = 0
        counter = 0
        while not (x_vector_period and y_vector_period and z_vector_period):
            counter += 1
            self.move_moons()
            if not x_vector_period and x_vectors_init == self.act_vector_by_axis(0):
                x_vector_period = counter
            if not y_vector_period and y_vectors_init == self.act_vector_by_axis(1):
                y_vector_period = counter
            if not z_vector_period and z_vectors_init == self.act_vector_by_axis(2):
                z_vector_period = counter
        return lcm(x_vector_period, y_vector_period, z_vector_period)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    s = CSpace()
    for i, (x, y, z) in enumerate(yield_input_data(p_input_file_path, p_chars_to_space='<>xyz,=')):
        s.add_item(Position3D(x, y, z), i)

    for _ in range(1000):
        s.move_moons()

    answer1 = s.act_energy
    answer2 = s.period_time

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 12, solve_puzzle)


if __name__ == '__main__':
    main()
