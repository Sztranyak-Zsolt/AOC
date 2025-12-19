import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    known_things_dict = {"children": 3, "cats": 7, "samoyeds": 2, "pomeranians": 3, "akitas": 0,
                         "vizslas": 0, "goldfish": 5, "trees": 3, "cars": 2, "perfumes": 1}
    answer1 = answer2 = None
    sue_dict = {}
    for _, sue_id, *item_list in yield_input_data(p_input_file_path, p_chars_to_space=':,'):
        sue_dict[sue_id] = {item_list[i]: item_list[i+1] for i in range(0, len(item_list), 2)}

    for sue_id, item_dict in sue_dict.items():
        for th, th_count in known_things_dict.items():
            if th in item_dict and item_dict[th] != th_count:
                break
        else:
            answer1 = sue_id
            break

    for sue_id, item_dict in sue_dict.items():
        for th, th_count in known_things_dict.items():
            if th not in item_dict:
                continue
            if th in ['cats', 'trees'] and item_dict[th] > th_count:
                continue
            if th in ['pomeranians', 'goldfish'] and item_dict[th] < th_count:
                continue
            if th not in ['pomeranians', 'goldfish', 'cats', 'trees'] and item_dict[th] == th_count:
                continue
            break
        else:
            answer2 = sue_id
            break

    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 16, solve_puzzle)


if __name__ == '__main__':
    main()
