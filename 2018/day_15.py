import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, add_positions
from collections import deque


class CCreature:
    def __init__(self, p_is_elf: bool, p_position: Position2D):
        self.hp = 200
        self.attack_power = 3
        self.is_elf = p_is_elf
        self.position = p_position

    def __lt__(self, other):
        return self.position.y > other.position.y \
            or self.position.y == other.position.y and self.position.x < other.position.x

    def __str__(self):
        return f'{"E" if self.is_elf else "G"} ({self.position.x},{self.position.y}): {self.hp} HP'


class CCombatGrid(CGridBase):
    order_list = [Position2D(0, 1), Position2D(-1, 0), Position2D(1, 0), Position2D(0, -1)]

    def __init__(self):
        super().__init__()
        self.starting_creature_list: list[CCreature] = []
        self.creature_list: list[CCreature] = []

    def reset_creatures(self, p_extra_elf_power: int = 0):
        self.creature_list = []
        for cr in self.starting_creature_list:
            self.creature_list.append(CCreature(cr.is_elf, cr.position))
        if p_extra_elf_power != 0:
            for elf in [elf for elf in self.creature_list if elf.is_elf]:
                elf.attack_power += p_extra_elf_power

    def get_move_direction(self, p_act_creature: CCreature, p_act_enemies: dict[Position2D, CCreature],
                           p_act_friends: dict[Position2D, CCreature]) -> Position2D:
        dq = deque([[p_act_creature.position, None, 0]])
        pos_cache = set()
        pos_cache.add(p_act_creature.position)
        closest_position = []
        prev_step_taken = 0
        while dq:
            act_position, starting_step, step_taken = dq.popleft()
            if step_taken != prev_step_taken and closest_position:
                return closest_position[1]
            prev_step_taken = step_taken
            for next_dir in self.order_list:
                np = add_positions(act_position, next_dir)
                if np in pos_cache or np in self.position_dict or np in p_act_friends:
                    continue
                pos_cache.add(np)
                if np in p_act_enemies:
                    if step_taken == 0:
                        return Position2D(0, 0)
                    if not closest_position:
                        closest_position = [np, starting_step]
                    else:
                        if np.y > closest_position[0].y \
                                or np.y == closest_position[0].y and np.x < closest_position[0].x:
                            closest_position = [np, starting_step]
                else:
                    dq.append([np, starting_step if step_taken != 0 else next_dir, step_taken + 1])
        return Position2D(0, 0)

    def get_attacked_enemy(self, p_act_creature: CCreature, p_act_enemies: dict[Position2D, CCreature]) -> CCreature:
        act_enemy: CCreature | None = None
        for next_dir in self.order_list:
            if (ap := add_positions(p_act_creature.position, next_dir)) in p_act_enemies:
                if act_enemy is None or act_enemy.hp > p_act_enemies[ap].hp:
                    act_enemy = p_act_enemies[ap]
        return act_enemy

    def attack_creature(self, p_creature: CCreature, p_attacked_creature: CCreature | None):
        if p_attacked_creature is None:
            return
        p_attacked_creature.hp = max(0, p_attacked_creature.hp - p_creature.attack_power)
        if p_attacked_creature.hp == 0:
            self.creature_list.remove(p_attacked_creature)

    def creature_turn(self, p_creature: CCreature):
        if p_creature.hp == 0:
            return
        enemies_dict = {c.position: c for c in self.creature_list if c.is_elf != p_creature.is_elf}
        friends_dict = {c.position: c for c in self.creature_list if c.is_elf == p_creature.is_elf
                        and c is not p_creature}
        p_creature.position = add_positions(p_creature.position,
                                            self.get_move_direction(p_creature, enemies_dict, friends_dict))
        self.attack_creature(p_creature, self.get_attacked_enemy(p_creature, enemies_dict))

    def combat_turn(self):
        creature_order = sorted(self.creature_list)
        for act_creature in creature_order:
            self.creature_turn(act_creature)

    @property
    def combat_finished(self) -> bool:
        return len(set([c.is_elf for c in self.creature_list if c.hp > 0])) == 1

    def combat(self, p_elf_extra_power: int = 0) -> int:
        self.reset_creatures(p_elf_extra_power)
        turn_counter = 0
        while not self.combat_finished:
            turn_counter += 1
            self.combat_turn()
        return turn_counter - 1

    def __str__(self):
        ret_lst = list()
        creature_positions = {k.position: k for k in self.creature_list if k.hp != 0}
        for d_y in range(self.max_y, self.min_y - 1, -1):
            d_act_row = ''
            extra_info = "  "
            for d_x in range(self.min_x, self.max_x + 1):
                if (d_x, d_y) in creature_positions:
                    if creature_positions[(d_x, d_y)].is_elf:
                        d_cr_str = 'E'
                        d_act_row += 'E'
                    else:
                        d_cr_str = 'G'
                        d_act_row += 'G'
                    extra_info += f"{d_cr_str} ({creature_positions[(d_x, d_y)].hp})  "
                elif (d_x, d_y) in self.position_dict:
                    d_act_row += str(self.position_dict[(d_x, d_y)])
                else:
                    d_act_row += '.'
            ret_lst.append(d_act_row + extra_info)
        return '\n'.join(ret_lst)


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    g = CCombatGrid()
    for inp_row in yield_input_data(p_input_file_path, p_reversed=True, p_whole_row=True):
        g.add_row(inp_row, p_chars_to_skip='EG.')
        if 'E' in inp_row or 'G' in inp_row:
            for x, c in enumerate(inp_row):
                if c in 'EG':
                    g.starting_creature_list.append(CCreature(c == 'E', Position2D(x, g.max_y)))

    g.reset_creatures()
    ct = g.combat()
    answer1 = ct * sum([k.hp for k in g.creature_list])

    extra_power = 1
    while True:
        ct = g.combat(extra_power)
        if len([elf for elf in g.creature_list if elf.is_elf and elf.hp > 0]) == \
                len([elf for elf in g.starting_creature_list if elf.is_elf]):
            answer2 = ct * sum([k.hp for k in g.creature_list])
            break
        extra_power += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 15, solve_puzzle)


if __name__ == '__main__':
    main()
