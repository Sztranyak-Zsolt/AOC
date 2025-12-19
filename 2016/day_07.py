import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from re import match


class CIPAddress:
    def __init__(self, p_ip_address):
        self.ip_address = p_ip_address

    @property
    def is_support_abba(self) -> bool:
        bracket_pattern = '.*\\[[^]]*(.)((?!\\1).)\\2\\1.*\\]'
        all_pattern = '.*(.)((?!\\1).)\\2\\1.*'
        return match(bracket_pattern, self.ip_address) is None and match(all_pattern, self.ip_address) is not None

    @property
    def is_support_aba(self) -> bool:
        aba1_pattern = '.*\\[[^]]*(.)((?!\\1).)\\1.*\\][^[]*\\2\\1\\2'
        aba2_pattern = '[^[]*(.)((?!\\1).)\\1.*\\[[^]]*\\2\\1\\2.*\\]'
        aba3_pattern = '.*\\][^[]*(.)((?!\\1).)\\1.*\\[[^]]*\\2\\1\\2.*\\]'
        return match(aba1_pattern, self.ip_address) is not None \
            or match(aba2_pattern, self.ip_address) is not None \
            or match(aba3_pattern, self.ip_address) is not None


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer1 = answer2 = 0
    for ip_address in yield_input_data(p_input_file_path, p_whole_row=True):
        new_ip = CIPAddress(ip_address)
        if new_ip.is_support_abba:
            answer1 += 1
        if new_ip.is_support_aba:
            answer2 += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 7, solve_puzzle)


if __name__ == '__main__':
    main()
