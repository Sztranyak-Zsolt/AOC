from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import CVector3D


def sign(n: int):
    if n > 0:
        return 1
    if n == 0:
        return 0
    return -1


class CParticle:
    def __init__(self, p_id: int,
                 p_position: CVector3D,
                 p_velocity: CVector3D,
                 p_acceleration: CVector3D):
        self.id = p_id
        self.position = p_position
        self.velocity = p_velocity
        self.acceleration = p_acceleration

    def get_next_phase(self) -> CParticle:
        next_phase_particle = CParticle(self.id, self.position, self.velocity, self.acceleration)
        next_phase_particle.velocity = next_phase_particle.velocity + next_phase_particle.acceleration
        next_phase_particle.position = next_phase_particle.position + next_phase_particle.velocity
        return next_phase_particle

    def __lt__(self, other: CParticle):
        a1 = int(self.acceleration)
        a2 = int(other.acceleration)
        v1 = v2 = 0
        for i in range(3):
            if sign(self.velocity[i]) == sign(self.acceleration[i]) or self.acceleration[i] == 0:
                v1 += abs(self.velocity[i])
            else:
                v1 -= abs(self.velocity[i])
            if sign(other.velocity[i]) == sign(other.acceleration[i]) or other.acceleration[i] == 0:
                v2 += abs(other.velocity[i])
            else:
                v2 -= abs(other.velocity[i])
        return (a1, v1) < (a2, v2)

    def __str__(self):
        return f'p={self.position}, v={self.velocity}, a={self.acceleration}'


class CParticleHandler:
    def __init__(self):
        self.particle_list: list[CParticle] = []

    def get_next_state(self):
        new_pl = []
        position_set = set()
        collision_set = set()
        for np in self.particle_list:
            new_pl.append(np.get_next_phase())
            if new_pl[-1].position in position_set:
                collision_set.add(new_pl[-1].position)
            position_set.add(new_pl[-1].position)
        for np in new_pl[::-1]:
            if np.position in collision_set:
                new_pl.remove(np)
        self.particle_list = new_pl


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    ph = CParticleHandler()
    for particle_id, inp_row in enumerate(yield_input_data(p_input_file_path, p_chars_to_space='pva=<>,',
                                                           p_only_nums=True)):
        ph.particle_list.append(CParticle(particle_id, CVector3D(*inp_row[:3]),
                                          CVector3D(*inp_row[3:6]), CVector3D(*inp_row[6:])))
    answer1 = min(ph.particle_list).id

    for i in range(100):
        ph.get_next_state()

    answer2 = len(ph.particle_list)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 20, solve_puzzle)


if __name__ == '__main__':
    main()
