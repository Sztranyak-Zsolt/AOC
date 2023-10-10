from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from itertools import permutations


class CGuest:
    def __init__(self, p_name):
        self.name = p_name
        self.sympathy_dict: dict[CGuest, int] = dict()


class CGuestHandler:
    def __init__(self):
        self.guest_dict: dict[str, CGuest] = {}

    def get_guest(self, p_guest_name):
        if p_guest_name not in self.guest_dict:
            self.guest_dict[p_guest_name] = CGuest(p_guest_name)
        return self.guest_dict[p_guest_name]

    def get_optimal_set(self):
        max_happiness = None
        perm_list = list(permutations(self.guest_dict.values()))
        for guest_permutation in perm_list:
            act_happiness = 0
            prev_guest = guest_permutation[-1]
            for act_guest in guest_permutation:
                act_happiness += prev_guest.sympathy_dict[act_guest]
                act_happiness += act_guest.sympathy_dict[prev_guest]
                prev_guest = act_guest
            if max_happiness is None or act_happiness > max_happiness:
                max_happiness = act_happiness
        return max_happiness


def solve_puzzle(p_input_file_path: str) -> (int, int):
    gh = CGuestHandler()
    for from_guest, _, sympathy_direction, sympathy_score, *_, to_guest in \
            yield_input_data(p_input_file_path, p_chars_to_space='.'):
        if sympathy_direction == 'lose':
            sympathy_score *= -1
        gh.get_guest(from_guest).sympathy_dict[gh.get_guest(to_guest)] = sympathy_score
    answer1 = gh.get_optimal_set()
    guest_list = list(gh.guest_dict.keys())
    for act_guest in guest_list:
        gh.get_guest('Santa').sympathy_dict[gh.get_guest(act_guest)] = 0
        gh.get_guest(act_guest).sympathy_dict[gh.get_guest('Santa')] = 0
    answer2 = gh.get_optimal_set()
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 13, solve_puzzle)


if __name__ == '__main__':
    main()
