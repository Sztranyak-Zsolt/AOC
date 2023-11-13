from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from copy import copy
import heapq
import os


class CSpell:
    def __init__(self, p_name: str, p_code: str, p_mana_cost: int,
                 p_effect_last: int = 0, p_damage: int = 0, p_heal: int = 0, p_armor: int = 0,
                 p_mana_recharge: int = 0):
        self.name = p_name
        self.code = p_code
        self.mana_cost = p_mana_cost
        self.effect_last = p_effect_last
        self.damage = p_damage
        self.heal = p_heal
        self.armor = p_armor
        self.mana_recharge = p_mana_recharge
        self.instant_effect = p_effect_last == 0

    def __str__(self):
        return self.code


class CSpellBook:
    def __init__(self):
        self.spell_list: list[CSpell] = []


class CPlayer:
    def __init__(self, p_name, p_init_hp, p_init_damage, p_init_armor, p_init_mana):
        self.name = p_name
        self.init_hp = p_init_hp
        self.act_hp = p_init_hp
        self.init_damage = p_init_damage
        self.init_armor = p_init_armor
        self.init_mana = p_init_mana
        self.act_mana = p_init_mana
        self.active_spells: dict[CSpell, int] = {}

    @property
    def act_damage(self):
        return self.init_damage + sum([spell.damage for spell in self.active_spells])

    @property
    def act_armor(self):
        return self.init_armor + sum([spell.armor for spell in self.active_spells])

    def __str__(self):
        return f"|{self.name}|HP{self.act_hp}|M{self.act_mana}|" \
               f"{''.join([str(k) + str(v) for k, v in self.active_spells.items()])}|"

    def __copy__(self):
        new_player = CPlayer(self.name, self.init_hp, self.init_damage, self.init_armor, self.init_mana)
        new_player.act_hp = self.act_hp
        new_player.act_mana = self.act_mana
        new_player.active_spells = copy(self.active_spells)
        return new_player


class CTurnState:
    def __init__(self, p_act_me: CPlayer, p_act_boss: CPlayer, p_is_hard: bool = False):
        self.act_me = p_act_me
        self.act_boss = p_act_boss
        self.winner: CPlayer | None = None
        self.mana_spent = 0
        self.is_hard = p_is_hard

    @property
    def state_code(self) -> str:
        return f'{self.act_me} {self.act_boss} {self.mana_spent} {self.is_hard}'

    def calculate_spells_effect(self):
        active_spell_keys = list(self.act_me.active_spells.keys())
        self.act_me.act_mana += sum([spell.mana_recharge for spell in self.act_me.active_spells])
        self.act_boss.act_hp -= sum([spell.damage for spell in self.act_me.active_spells])
        for act_spell in active_spell_keys:
            if self.act_me.active_spells[act_spell] == 1:
                del self.act_me.active_spells[act_spell]
            else:
                self.act_me.active_spells[act_spell] -= 1

    def take_my_turn(self, p_next_spell: CSpell):
        if self.is_hard:
            self.act_me.act_hp -= 1
            if self.act_me == 0:
                return
        self.calculate_spells_effect()
        self.act_me.act_mana = self.act_me.act_mana - p_next_spell.mana_cost
        self.mana_spent += p_next_spell.mana_cost
        if self.act_me.act_mana < 0 or p_next_spell in self.act_me.active_spells:
            return
        if not p_next_spell.instant_effect:
            self.act_me.active_spells[p_next_spell] = p_next_spell.effect_last
            return
        self.act_me.act_hp += p_next_spell.heal
        self.act_boss.act_hp -= p_next_spell.damage

    def take_boss_turn(self):
        self.calculate_spells_effect()
        if self.act_boss.act_hp <= 0:
            return
        self.act_me.act_hp -= max(1, self.act_boss.act_damage - self.act_me.act_armor)

    def calc_winner(self):
        if self.act_me.act_hp <= 0 or self.act_me.act_mana < 0:
            self.winner = self.act_boss
        elif self.act_boss.act_hp <= 0:
            self.winner = self.act_me

    def get_next_turn(self, p_next_spell: CSpell):
        new_state = copy(self)
        new_state.take_my_turn(p_next_spell)
        new_state.calc_winner()
        if new_state.winner is None:
            new_state.take_boss_turn()
            new_state.calc_winner()
        return new_state

    def __copy__(self):
        new_state = CTurnState(copy(self.act_me), copy(self.act_boss), self.is_hard)
        new_state.mana_spent = self.mana_spent
        new_state.winner = self.winner
        return new_state

    def __lt__(self, other):
        return self.mana_spent < other.mana_spent


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = None
    input_iter = iter(yield_input_data(p_input_file_path))
    me = CPlayer("Me", 50, 0, 0, 500)
    boss = CPlayer("BOSS", next(input_iter)[-1], next(input_iter)[-1], 0, 0)
    spellbook = CSpellBook()
    for spell_row in yield_input_data(os.path.join(os.path.dirname(__file__), 'input/input_201522_spells.txt')):
        spellbook.spell_list.append(CSpell(*spell_row))

    game_state = CTurnState(me, boss, False)
    game_states_pq = [game_state]

    heapq.heapify(game_states_pq)
    known_turns = set()
    while game_states_pq:
        act_state = heapq.heappop(game_states_pq)
        if act_state.state_code in known_turns:
            continue
        known_turns.add(act_state.state_code)
        if act_state.winner == act_state.act_me:
            answer1 = act_state.mana_spent
            break
        for next_spell in spellbook.spell_list:
            next_state = act_state.get_next_turn(next_spell)
            if next_state.winner is None or next_state.winner == next_state.act_me:
                heapq.heappush(game_states_pq, next_state)

    game_state_hard = CTurnState(me, boss, True)
    game_states_pq = [game_state_hard]

    heapq.heapify(game_states_pq)
    known_turns = set()
    while game_states_pq:
        act_state = heapq.heappop(game_states_pq)
        if act_state.state_code in known_turns:
            continue
        known_turns.add(act_state.state_code)
        if act_state.winner == act_state.act_me:
            answer2 = act_state.mana_spent
            break
        for next_spell in spellbook.spell_list:
            next_state = act_state.get_next_turn(next_spell)
            if next_state.winner is None or next_state.winner == next_state.act_me:
                heapq.heappush(game_states_pq, next_state)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 22, solve_puzzle)


if __name__ == '__main__':
    main()
