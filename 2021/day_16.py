from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from math import prod


def gte(num: list[int]) -> int:
    if num[0] > num[1]:
        return 1
    return 0


def lte(num: list[int]) -> int:
    if num[0] < num[1]:
        return 1
    return 0


def eq(num: list[int]) -> int:
    if num[0] == num[1]:
        return 1
    return 0


def hex_to_bin(p_hex: str) -> str:
    return bin(int(p_hex, 16))[2:].zfill(len(p_hex) * 4)


class CPacket:
    def __init__(self, p_code: str):
        self.version = 0
        self.type_id = 0
        self.length_type_id = 0
        self.packet_header_length = 0
        self.literal_value = 0
        self.literal_length = 0
        self.sub_packet_list: list[CPacket] = list()
        self.code = p_code

    @property
    def code(self) -> str:
        return self._code[:self.packet_full_length]

    @code.setter
    def code(self, p_code: str):
        self._code = p_code
        self.version = int(p_code[:3], 2)
        self.type_id = int(p_code[3:6], 2)
        if self.type_id == 4:
            self.packet_header_length = 6
            self.calc_literal_value(p_code[6:])
            return
        self.length_type_id = int(p_code[6])
        if self.length_type_id:
            self.packet_header_length = 18
            self.add_subpackage_by_count(p_code[18:], int(p_code[7:18], 2))
        else:
            self.packet_header_length = 22
            self.add_package_by_length(p_code[22:], int(p_code[7:22], 2))

    @property
    def packet_full_length(self) -> int:
        if not self.sub_packet_list:
            return self.packet_header_length + self.literal_length
        return self.packet_header_length + sum([p.packet_full_length for p in self.sub_packet_list])

    def add_subpackage_by_count(self, p_bin: str, p_count: int):
        while len(self.sub_packet_list) != p_count:
            self.sub_packet_list.append(CPacket(p_bin))
            p_bin = p_bin[self.sub_packet_list[-1].packet_full_length:]

    def add_package_by_length(self, p_bin: str, p_length: int):
        while not self.sub_packet_list or p_length > sum([p.packet_full_length for p in self.sub_packet_list]):
            self.sub_packet_list.append(CPacket(p_bin))
            p_bin = p_bin[self.sub_packet_list[-1].packet_full_length:]

    def calc_literal_value(self, p_binary: str):
        to_continue = 1
        all_part = ''
        while to_continue:
            to_continue, act_part, p_binary = int(p_binary[0]), p_binary[1:5], p_binary[5:]
            all_part += act_part
            self.literal_length += 5
        self.literal_value = int(all_part, 2)

    def calc_all_version(self):
        return self.version + sum([x.calc_all_version() for x in self.sub_packet_list])

    def __int__(self):
        if self.type_id == 4:
            return self.literal_value
        op_dict = {0: sum, 1: prod, 2: min, 3: max, 5: gte, 6: lte, 7: eq}
        return op_dict[self.type_id]([int(sp) for sp in self.sub_packet_list])


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    input_iterator = iter(yield_input_data(p_input_file_path, p_whole_row=True))
    cp = CPacket(hex_to_bin(next(input_iterator)))
    answer1 = cp.calc_all_version()
    answer2 = int(cp)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 16, solve_puzzle)


if __name__ == '__main__':
    main()
