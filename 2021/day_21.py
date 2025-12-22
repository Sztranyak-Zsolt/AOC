import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from collections import defaultdict
from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from functools import cache
from itertools import product


@cache
def dirac_dice_roll3() -> dict[int, int]:
    rd = {}
    for roll3_possibility in product((1, 2, 3), repeat=3):
        if sum(roll3_possibility) not in rd:
            rd[sum(roll3_possibility)] = 1
        else:
            rd[sum(roll3_possibility)] += 1
    return rd


class CDice:
    def __init__(self):
        self.act_value = 1
        self.roll_count = 0

    def roll3(self) -> int:
        rv = 0
        for _ in range(3):
            rv += self.act_value
            self.act_value = self.act_value % 100 + 1
            self.roll_count += 1
        return rv


class CPlayer:
    def __init__(self, p_starting_position: int):
        self.score = 0
        self.starting_position = p_starting_position
        self.actual_position = p_starting_position
        self.turn_to_win = defaultdict(lambda: 0)
        self.turn_to_still_not_win = defaultdict(lambda: 0)

    def add_step(self, p_step: int):
        self.actual_position = (self.actual_position + p_step - 1) % 10 + 1
        self.score += self.actual_position

    def calc_turns_to_win(self):
        active_turn_poss_count = {(self.starting_position, 0): 1}
        turn_to_win = {}
        act_turn = 0
        while active_turn_poss_count:
            act_turn += 1
            new_turn_poss_count = defaultdict(lambda: 0)
            for (act_position, act_score), act_point_poss_counter in active_turn_poss_count.items():
                for rolled_value, rolled_poss in dirac_dice_roll3().items():
                    new_position = (act_position + rolled_value - 1) % 10 + 1
                    new_score = act_score + new_position
                    if new_score >= 21:
                        self.turn_to_win[act_turn] += act_point_poss_counter * rolled_poss
                        continue
                    self.turn_to_still_not_win[act_turn] += act_point_poss_counter * rolled_poss
                    new_turn_poss_count[(new_position, new_score)] += act_point_poss_counter * rolled_poss
            active_turn_poss_count = new_turn_poss_count
        return turn_to_win


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    input_iterator = iter(yield_input_data(p_input_file_path))
    p1_start, p2_start = next(input_iterator)[-1], next(input_iterator)[-1]
    dice = CDice()
    player1 = CPlayer(p1_start)
    player2 = CPlayer(p2_start)

    next_player = {player1: player2, player2: player1}
    act_player = player2
    while act_player.score < 1000:
        act_player = next_player[act_player]
        act_player.add_step(dice.roll3())
    answer1 = next_player[act_player].score * dice.roll_count

    player1.calc_turns_to_win()
    player2.calc_turns_to_win()

    p1_win_poss, p2_win_poss = 0, 0
    for p1_t, p1_c in player1.turn_to_win.items():
        p1_win_poss += p1_c * player2.turn_to_still_not_win[p1_t - 1]
    for p2_t, p2_c in player2.turn_to_win.items():
        p2_win_poss += p2_c * player1.turn_to_still_not_win[p2_t]
    answer2 = max(p1_win_poss, p2_win_poss)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 21, solve_puzzle)


if __name__ == '__main__':
    main()
