from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CBingoNumber:
    def __init__(self, p_value: int):
        self.value = p_value
        self.is_found = False


class CBingoTable:
    def __init__(self):
        self.bingo_table: list[list[CBingoNumber]] = []

    def is_bingo(self) -> bool:
        return self.is_row_bingo() or self.is_column_bingo()

    def is_row_bingo(self) -> bool:
        for b_row in self.bingo_table:
            if False not in [x.is_found for x in b_row]:
                return True
        return False

    def is_column_bingo(self) -> bool:
        c1, c2, c3, c4, c5 = True, True, True, True, True
        for b_row in self.bingo_table:
            c1 = c1 and b_row[0].is_found
            c2 = c2 and b_row[1].is_found
            c3 = c3 and b_row[2].is_found
            c4 = c4 and b_row[3].is_found
            c5 = c5 and b_row[4].is_found
        return c1 or c2 or c3 or c4 or c5

    def bingo_numbers_sum(self, p_is_found: bool = True) -> int:
        sum_num = 0
        for b_row in self.bingo_table:
            sum_num += sum([x.value for x in b_row if x.is_found == p_is_found])
        return sum_num


class CBingoHandler:
    def __init__(self):
        self.bingo_numbers: dict[int, CBingoNumber] = {x: CBingoNumber(x) for x in range(100)}
        self.draw_list: list[int] = []
        self.bingo_table_list: list[CBingoTable] = list()

    def add_bingo_table(self, p_bn_list: list[list[int]]):
        new_bingo_table = CBingoTable()
        for bingo_row in p_bn_list:
            new_bingo_table.bingo_table.append([self.bingo_numbers[n] for n in bingo_row])
        self.bingo_table_list.append(new_bingo_table)

    def reset_draw(self):
        for act_num in self.bingo_numbers:
            self.bingo_numbers[act_num].is_found = False

    @property
    def first_bingo_table_score(self):
        self.reset_draw()
        for next_draw in self.draw_list:
            self.bingo_numbers[next_draw].is_found = True
            for bt in self.bingo_table_list:
                if bt.is_bingo():
                    return bt.bingo_numbers_sum(False) * next_draw

    @property
    def last_bingo_table_score(self):
        self.reset_draw()
        winning_bingo_tables = []
        for next_draw in self.draw_list:
            self.bingo_numbers[next_draw].is_found = True
            for bt in self.bingo_table_list:
                if bt not in winning_bingo_tables and bt.is_bingo():
                    winning_bingo_tables.append(bt)
                    if len(winning_bingo_tables) == len(self.bingo_table_list):
                        return winning_bingo_tables[-1].bingo_numbers_sum(False) * next_draw


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    bh = CBingoHandler()
    for i, inp_group in enumerate(yield_input_data(p_input_file_path, p_group_separator='\n\n', p_chars_to_space=',')):
        if i == 0:
            bh.draw_list = inp_group[0]
        else:
            bh.add_bingo_table(inp_group)

    answer1 = bh.first_bingo_table_score
    answer2 = bh.last_bingo_table_score

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 4, solve_puzzle)


if __name__ == '__main__':
    main()
