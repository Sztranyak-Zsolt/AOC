from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CCombatDecks:
    def __init__(self, p_player1_deck: list[int] | None = None, p_player2_deck: list[int] | None = None):
        if p_player1_deck is None:
            self.player1_deck: list[int] = []
        else:
            self.player1_deck = p_player1_deck
        if p_player2_deck is None:
            self.player2_deck: list[int] = []
        else:
            self.player2_deck = p_player2_deck

    def combat_winner_deck(self) -> list[int]:
        deck_1 = self.player1_deck.copy()
        deck_2 = self.player2_deck.copy()
        while deck_1 and deck_2:
            a1, a2 = deck_1.pop(0), deck_2.pop(0)
            if a1 > a2:
                deck_1.extend([a1, a2])
            else:
                deck_2.extend([a2, a1])
        if deck_1:
            return deck_1
        return deck_2

    def recursive_combat(self, p_deck1: list[int] | None = None, p_deck2: list[int] | None = None) -> (bool, list[int]):
        if not p_deck1:
            p_deck1 = self.player1_deck.copy()
        if not p_deck2:
            p_deck2 = self.player2_deck.copy()
        p1_deck_list = list()
        while p_deck1 and p_deck2:
            if tuple(p_deck1) in p1_deck_list:
                break
            p1_deck_list.append(tuple(p_deck1))
            a1, a2 = p_deck1.pop(0), p_deck2.pop(0)
            if a1 <= len(p_deck1) and a2 <= len(p_deck2):
                if self.recursive_combat(p_deck1[:a1], p_deck2[:a2])[0]:
                    p_deck1.extend([a1, a2])
                else:
                    p_deck2.extend([a2, a1])
            elif a1 > a2:
                p_deck1.extend([a1, a2])
            else:
                p_deck2.extend([a2, a1])
        if p_deck1:
            return True, p_deck1
        return False, p_deck2


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    input_group = iter(yield_input_data(p_input_file_path, p_whole_row=True, p_group_separator='\n\n'))
    cd = CCombatDecks(next(input_group)[1:], next(input_group)[1:])

    answer1 = sum([i * v for i, v in enumerate(cd.combat_winner_deck()[::-1], start=1)])
    answer2 = sum([i * v for i, v in enumerate(cd.recursive_combat()[1][::-1], start=1)])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 22, solve_puzzle)


if __name__ == '__main__':
    main()
