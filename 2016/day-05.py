import hashlib
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CCodeGenerator:
    def __init__(self, p_door_id):
        self._door_id: str = ''
        self.code1 = ''
        self.code2 = ''
        self.door_id = p_door_id

    @property
    def door_id(self):
        return self._door_id

    @door_id.setter
    def door_id(self, value):
        self._door_id = value
        self.calc_code(8)

    def calc_code(self, p_code_length: int):
        code_string1 = ''
        code_string2 = ['_'] * p_code_length
        act_number_to_check = 0
        while True:
            act_number_to_check += 1
            string_to_hash = f'{self.door_id}{act_number_to_check}'
            hash_calc = hashlib.md5(string_to_hash.encode()).hexdigest()
            if hash_calc[:5] == '00000':
                if len(code_string1) < p_code_length:
                    code_string1 += hash_calc[5]
                    if len(code_string1) == p_code_length:
                        self.code1 = code_string1
                if hash_calc[5] in '01234567' and code_string2[int(hash_calc[5])] == '_':
                    code_string2[int(hash_calc[5])] = hash_calc[6]
                    if '_' in code_string2:
                        continue
                    self.code2 = ''.join(code_string2)
                    break


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    door = CCodeGenerator(next(yield_input_data(p_input_file_path, p_whole_row=True), None))
    answer1 = door.code1
    answer2 = door.code2

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 5, solve_puzzle)


if __name__ == '__main__':
    main()
