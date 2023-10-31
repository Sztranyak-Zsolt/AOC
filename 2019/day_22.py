from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CDeckCard:
    def __init__(self, p_value: int, p_deck_length: int):
        self.value = p_value
        self.position = p_value
        self.deck_length = p_deck_length

    def cut_deck(self, p_cut: int):
        self.position = (self.position - p_cut) % self.deck_length

    def deal_new_stack(self):
        self.position = self.deck_length - self.position - 1

    def deal_with_incr(self, p_incr_num: int):
        self.position = (self.position * p_incr_num) % self.deck_length


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    d = CDeckCard(2019, 10007)
    for inp_row in yield_input_data(p_input_file_path):
        if inp_row[0] == 'cut':
            d.cut_deck(inp_row[1])
        elif inp_row[2] == 'increment':
            d.deal_with_incr(inp_row[3])
        else:
            d.deal_new_stack()
    answer1 = d.position

    factory_deck_number2 = 119315717514047
    shuffle_count = 101741582076661

    d0 = CDeckCard(0, factory_deck_number2)
    d1 = CDeckCard(1, factory_deck_number2)

    # shuffle results linear transformation; y = (a + b * x) % m
    # where 'a' can be calculated as position of card0 after 1 shuffle
    # and 'b' equals the difference between card 1 and card 0 after 1 shuffle

    for act_instr in yield_input_data(p_input_file_path):
        if act_instr[0] == 'cut':
            d0.cut_deck(act_instr[1])
            d1.cut_deck(act_instr[1])
        elif act_instr[2] == 'increment':
            d0.deal_with_incr(act_instr[3])
            d1.deal_with_incr(act_instr[3])
        else:
            d0.deal_new_stack()
            d1.deal_new_stack()
    a = d0.position
    b = d1.position - d0.position

    x = 2020
    # result is card 2020 shuffle reversed -> that card will arrive in position 2020
    act_num = factory_deck_number2 - shuffle_count - 1

    while act_num != 0:
        act_mod = act_num % 2
        act_num = act_num // 2
        if act_mod == 1:
            x = (a + x * b) % factory_deck_number2
        # transformation of the next 2 power 'a' and 'b' is:
        # (a + b * (a + x * b)) % m = ((a + b * a) % m + (b ** 2) % m * x) % m
        # new a = (a + b * a) % m, new b = (b ** 2) % m
        a, b = (a + b * a) % factory_deck_number2, (b ** 2) % factory_deck_number2
    answer2 = x

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 22, solve_puzzle)


if __name__ == '__main__':
    main()
