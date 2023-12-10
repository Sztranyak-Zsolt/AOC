from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    hands = []
    hands2 = []
    card_strength_dict = {str(s): s for s in range(2, 10)} | {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    card_strength_dict2 = card_strength_dict | {'J': 1}

    for hand, bid in yield_input_data(p_input_file_path, p_convert_to_num=False):
        act_hand_strength = sorted([hand.count(c) for c in set(hand)], reverse=True)
        act_hand_strength2 = act_hand_strength.copy()
        if j_count := hand.count('J'):
            act_hand_strength2.remove(j_count)
            if act_hand_strength2:
                act_hand_strength2[0] += j_count
            else:
                act_hand_strength2.append(5)
        hands.append([act_hand_strength, [card_strength_dict[s] for s in hand], hand, int(bid)])
        hands2.append([act_hand_strength2, [card_strength_dict2[s] for s in hand], hand, int(bid)])

    answer1 = sum(i * b[3] for i, b in enumerate(sorted(hands), start=1))
    answer2 = sum(i * b[3] for i, b in enumerate(sorted(hands2), start=1))
    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 7, solve_puzzle)


if __name__ == '__main__':
    main()
