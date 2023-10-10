from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from re import fullmatch
from string import ascii_lowercase


class CRoomCode:
    def __init__(self, p_code: str, p_sector_code: int):
        self.code = p_code
        self.sector_code = p_sector_code

    @property
    def room_name(self) -> str:
        room_name = ''
        divisor = len(ascii_lowercase)
        for act_code in self.code:
            if act_code == "-":
                room_name += ' '
            else:
                act_index = ascii_lowercase.index(act_code) + 1
                new_index = (act_index + self.sector_code) % divisor - 1
                room_name += ascii_lowercase[new_index]
        return room_name

    @property
    def checksum(self) -> str:
        letter_dict = dict()
        for act_code in self.code.replace("-", ""):
            if act_code in letter_dict:
                letter_dict[act_code] += 1
            else:
                letter_dict[act_code] = 1
        a = [k for k, v in sorted(letter_dict.items(), key=lambda item: [-item[1], item[0]])]
        return ''.join(a[:5])


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    for room_raw_code in yield_input_data(p_input_file_path, p_whole_row=True):
        room_match = fullmatch(r"([a-z\-]+)-([0-9]+)\[([a-z]{5})]", room_raw_code)
        new_room = CRoomCode(room_match[1], int(room_match[2]))
        if new_room.checksum == room_match[3]:
            answer1 += new_room.sector_code
            if new_room.room_name == "northpole object storage":
                answer2 = new_room.sector_code

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 4, solve_puzzle)


if __name__ == '__main__':
    main()
