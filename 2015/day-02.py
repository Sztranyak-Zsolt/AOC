from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int, int):

    def calc_paper_need(p_length: int, p_width: int, p_height: int) -> int:
        return 2 * (p_length * p_width + p_length * p_height + p_width * p_height) \
            + p_length * p_width * p_height // max(p_length, p_width, p_height)

    def calc_ribbon_need(p_length: int, p_width: int, p_height: int) -> int:
        return 2 * (p_length + p_height + p_width - max(p_length, p_width, p_height)) + p_length * p_width * p_height

    paper_need, ribbon_need = 0, 0
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='x'):
        inp_row_length, inp_row_weight, inp_row_height = inp_row
        paper_need += calc_paper_need(inp_row_length, inp_row_weight, inp_row_height)
        ribbon_need += calc_ribbon_need(inp_row_length, inp_row_weight, inp_row_height)

    return paper_need, ribbon_need


def main():
    aoc_solve_puzzle(2015, 2, solve_puzzle)


if __name__ == '__main__':
    main()
