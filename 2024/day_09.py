from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from copy import deepcopy


class CDisk:
    def __init__(self):
        self.original_data: list[list[int, int, int]] = []  # file_id, file_length, space_length

    def serialize_raw(self, p_raw_data: str) -> None:
        act_file_id = 0
        act_raw_id = 0
        while act_raw_id != len(p_raw_data):
            file_sector_count = int(p_raw_data[act_raw_id])
            act_raw_id += 1
            if act_raw_id != len(p_raw_data):
                empty_sector_count = int(p_raw_data[act_raw_id])
                act_raw_id += 1
            else:
                empty_sector_count = 0
            self.original_data.append([act_file_id, file_sector_count, empty_sector_count])
            act_file_id += 1

    def format1(self):
        act_start_index = 0
        last_file_index, last_file_count, _ = self.original_data.pop()
        while act_start_index < len(self.original_data):
            act_file_index, act_file_count, act_empty_count = self.original_data[act_start_index]
            if act_empty_count == 0:
                act_start_index += 1
                continue
            self.original_data[act_start_index][2] = 0
            act_start_index += 1
            sectors_to_move = min(last_file_count, act_empty_count)
            self.original_data.insert(act_start_index, [last_file_index, sectors_to_move, act_empty_count - sectors_to_move])
            last_file_count -= sectors_to_move
            if last_file_count == 0:
                last_file_index, last_file_count, _ = self.original_data.pop()
        self.original_data.append([last_file_index, last_file_count, 0])

    def format2(self):
        act_end_index = len(self.original_data) - 1
        act_file_id, act_file_count, act_empty_count = self.original_data[act_end_index]
        while act_file_id:
            act_start_index = 0
            while act_start_index < act_end_index:
                if self.original_data[act_start_index][2] - act_file_count >= 0:
                    self.original_data[act_end_index - 1][2] += act_file_count + act_empty_count
                    next_empty_count = self.original_data[act_start_index][2] - act_file_count
                    self.original_data[act_start_index][2] = 0
                    self.original_data.pop(act_end_index)
                    self.original_data.insert(act_start_index + 1, [act_file_id, act_file_count, next_empty_count])
                    break
                act_start_index += 1
            act_file_id -= 1
            while self.original_data[act_end_index][0] != act_file_id:
                act_end_index -= 1
            _, act_file_count, act_empty_count = self.original_data[act_end_index]

    @property
    def checksum(self) -> int:
        rv = 0
        act_index = 0
        for file_id, file_count, empty_count in self.original_data:
            rv += (act_index + (act_index + file_count - 1)) * file_count // 2 * file_id
            act_index += file_count + empty_count
        return rv

    def __deepcopy__(self, p_memo):
        new_instance = self.__new__(self.__class__)
        new_instance.original_data = deepcopy(self.original_data)
        return new_instance


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    input_iterator = iter(yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False))
    input_single_row = next(input_iterator)

    d = CDisk()
    d.serialize_raw(input_single_row)

    d2 = deepcopy(d)
    d.format1()
    answer1 = d.checksum

    d2.format2()
    answer2 = d2.checksum

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 9, solve_puzzle)


if __name__ == '__main__':
    main()
