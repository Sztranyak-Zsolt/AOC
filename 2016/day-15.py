from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CDisk:
    def __init__(self, p_id: int, p_position_count: int, p_time0_position: int):
        self.id = p_id
        self.position_count = p_position_count
        self.time0_position = p_time0_position

    def bounced(self, p_timer) -> bool:
        return (p_timer + self.time0_position) % self.position_count == 0


class CDiskHandler:
    def __init__(self):
        self.disk_list: list[CDisk] = list()

    def calc_perfect_timing(self) -> int:
        act_timer = 0
        while not all([x.bounced(act_timer + i + 1) for i, x in enumerate(self.disk_list)]):
            act_timer += 1
        return act_timer


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    dh = CDiskHandler()
    for _, disk_id, _, position_count, *_, st_position in yield_input_data(p_input_file_path, p_chars_to_space='#.'):
        dh.disk_list.append(CDisk(disk_id, position_count, st_position))

    answer1 = dh.calc_perfect_timing()

    dh.disk_list.append(CDisk(7, 11, 0))
    answer2 = dh.calc_perfect_timing()

    return answer1, answer2


def main():
    aoc_solve_puzzle(2016, 15, solve_puzzle)


if __name__ == '__main__':
    main()
