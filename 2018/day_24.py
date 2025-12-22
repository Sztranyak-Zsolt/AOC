from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from copy import copy


class CUnit:
    def __init__(self, p_hp: int, p_initiative: int, p_damage: int, p_unit_damage_type: str,
                 weakness_immunity_list_raw: list[str]):
        self.initiative: int = p_initiative
        self.hit_points: int = p_hp
        self.attack_damage: int = p_damage
        self.attack_type: str = p_unit_damage_type
        self.weaknesses: list[str] = []
        self.immunities: list[str] = []
        act_wi_list = []
        for act_wi in weakness_immunity_list_raw:
            if act_wi == 'to':
                continue
            elif act_wi == 'weak':
                act_wi_list = self.weaknesses
            elif act_wi == 'immune':
                act_wi_list = self.immunities
            else:
                act_wi_list.append(act_wi)

    def __str__(self):
        imm_w = []
        imm_w_str = ''
        if self.immunities:
            imm_w.append("immune to " + ", ".join(self.immunities))
        if self.weaknesses:
            imm_w.append("weak to " + ", ".join(self.weaknesses))
        if imm_w:
            imm_w_str = "(" + "; ".join(imm_w) + ") "
        return f"{self.hit_points} hit points {imm_w_str}" \
               f"with an attack that does {self.attack_damage} {self.attack_type} damage " \
               f"at initiative {self.initiative}"


class CArmy:
    def __init__(self, p_army_name: str):
        self.army_name = p_army_name
        self.unit_dict: dict[CUnit, int] = {}

    def __copy__(self):
        new_instance = CArmy(self.army_name)
        new_instance.unit_dict = self.unit_dict.copy()
        return new_instance

    def __str__(self):
        rs = self.army_name + ":"
        for unit, unit_count in self.unit_dict.items():
            rs += f'\n{unit_count} units each with {unit}'
        return rs

    def __int__(self):
        return sum(self.unit_dict.values())


class CCombat:
    def __init__(self, p_army1: CArmy, p_army2: CArmy, p_army1_boost: int = 0, p_army2_boost: int = 0):
        self.army1: CArmy = copy(p_army1)
        self.army1_boost = p_army1_boost
        self.army2: CArmy = copy(p_army2)
        self.army2_boost = p_army2_boost

    @property
    def winner(self) -> CArmy | None:
        while True:
            act_sum_hp = int(self.army1) + int(self.army2)
            self.targeting()
            self.attacking()
            if int(self.army1) == 0:
                return self.army2
            if int(self.army2) == 0:
                return self.army1
            if act_sum_hp == int(self.army1) + int(self.army2):
                return None

    def targeting(self) -> dict[CUnit, tuple[CUnit, bool]]:
        rd = {}
        for act_attack_army, act_defender_army in [(self.army1, self.army2), (self.army2, self.army1)]:
            selected_defenders = set()
            if act_attack_army == self.army1:
                att_boost = self.army1_boost
                def_boost = self.army2_boost
            else:
                att_boost = self.army2_boost
                def_boost = self.army1_boost
            for attacker, _ in sorted(act_attack_army.unit_dict.items(),
                                      key=lambda x: ((x[0].attack_damage + att_boost) * x[1], x[0].initiative),
                                      reverse=True):
                for attacked, _ in sorted(act_defender_army.unit_dict.items(),
                                          key=lambda x: (attacker.attack_type in x[0].weaknesses,
                                                         (x[0].attack_damage + def_boost) * x[1],
                                                         x[0].initiative),
                                          reverse=True):
                    if attacked not in selected_defenders and act_defender_army.unit_dict[attacked] != 0 \
                            and attacker.attack_type not in attacked.immunities:
                        rd[attacker] = (attacked, act_attack_army == self.army1)
                        selected_defenders.add(attacked)
                        break
        return rd

    def attacking(self):
        act_targeting = self.targeting()
        for act_attacker, (act_attacked, is_army1) in sorted(act_targeting.items(), key=lambda l: -l[0].initiative):
            if is_army1:
                attacker_army = self.army1
                att_boost = self.army1_boost
                defender_army = self.army2
            else:
                attacker_army = self.army2
                att_boost = self.army2_boost
                defender_army = self.army1
            act_damage = (act_attacker.attack_damage + att_boost) * attacker_army.unit_dict[act_attacker]
            if act_attacker.attack_type in act_attacked.weaknesses:
                act_damage *= 2
            defender_army.unit_dict[act_attacked] = max(0, defender_army.unit_dict[act_attacked] -
                                                        act_damage // act_attacked.hit_points)


def calc_min_boost_winner(p_immune_system: CArmy, p_infection: CArmy) -> CArmy:
    act_boost = 0
    while True:
        act_winner = CCombat(p_immune_system, p_infection, act_boost).winner
        if act_winner is None or act_winner.army_name != p_immune_system.army_name:
            act_boost += 1
            continue
        break
    return act_winner


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    immune_system = CArmy('Immune system')
    infection = CArmy('Infection')
    for i, inp_group in enumerate(
            yield_input_data(p_input_file_path, p_group_separator='\n\n', p_chars_to_space='(),;')):
        if i == 0:
            act_combat_member = immune_system
        else:
            act_combat_member = infection
        for act_unit in inp_group[1:]:
            unit_count, _, _, _, unit_hp, _, _, *immunities, _, _, _, _, _, \
                unit_damage, unit_damage_type, _, _, _, unit_initiative = act_unit
            new_unit = CUnit(unit_hp, unit_initiative, unit_damage, unit_damage_type, immunities)
            act_combat_member.unit_dict[new_unit] = unit_count
    c = CCombat(immune_system, infection)
    answer1 = int(c.winner)
    answer2 = int(calc_min_boost_winner(immune_system, infection))
    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 24, solve_puzzle)


if __name__ == '__main__':
    main()
