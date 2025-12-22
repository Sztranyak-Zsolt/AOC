import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from re import fullmatch


class CPassport:
    def __init__(self):
        self.info_dict: dict[str, str | int | tuple[int, str]] = {}

    @property
    def has_all_fields(self) -> bool:
        return len({'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'} & set(self.info_dict)) == 7

    @property
    def is_valid(self) -> bool:
        if not self.has_all_fields:
            return False
        if not 1920 <= self.info_dict['byr'] <= 2002:
            return False
        if not 2010 <= self.info_dict['iyr'] <= 2020:
            return False
        if not 2020 <= self.info_dict['eyr'] <= 2030:
            return False
        if not (150 <= self.info_dict['hgt'][0] <= 193 and self.info_dict['hgt'][1]== 'cm'
                or 59 <= self.info_dict['hgt'][0] <= 76 and self.info_dict['hgt'][1] == 'in'):
            return False
        if not fullmatch(r'#[0-9a-f]{6}', self.info_dict['hcl']):
            return False
        if not self.info_dict['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            return False
        if not fullmatch(r'[0-9]{9}', self.info_dict['pid']):
            return False
        return True

    def set_info_from_raw(self, p_info_list: list[list[str]]):
        for info_row in p_info_list:
            for info in info_row:
                k, v = info.split(':')
                if k in ['byr', 'iyr', 'eyr']:
                    try:
                        self.info_dict[k] = int(v)
                    except ValueError:
                        continue
                elif k in 'hgt':
                    if v[-2:] in ['in', 'cm']:
                        self.info_dict[k] = (int(v[:-2]), v[-2:])
                    else:
                        self.info_dict[k] = (int(v), '')
                else:
                    self.info_dict[k] = v


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    for act_group in yield_input_data(p_input_file_path, p_group_separator='\n\n'):
        p = CPassport()
        p.set_info_from_raw(act_group)
        if p.has_all_fields:
            answer1 += 1
        if p.is_valid:
            answer2 += 1
    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 4, solve_puzzle)


if __name__ == '__main__':
    main()
