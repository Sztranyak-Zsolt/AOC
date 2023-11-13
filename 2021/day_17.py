from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_vector import CVector2D


def shot_on_target(p_vector: CVector2D, p_x_range: CVector2D, p_y_range: CVector2D) -> bool:
    act_position = CVector2D(0, 0)
    while act_position[0] <= p_x_range[1] and act_position[1] >= p_y_range[0]:
        if act_position[0] >= p_x_range[0] and act_position[1] <= p_y_range[1]:
            return True
        act_position = act_position + p_vector
        p_vector = (max(0, p_vector[0] - 1), p_vector[1] - 1)
    return False


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = None
    answer2 = 0
    input_iterator = iter(yield_input_data(p_input_file_path, p_chars_to_space='.=,', p_only_nums=True))
    x1, x2, y1, y2 = next(input_iterator)
    for x in range(1, x2 + 1):
        for y in range(y1, -y1):  # solution based on negative y values
            if shot_on_target(CVector2D(x, y), CVector2D(x1, x2), CVector2D(y1, y2)):
                if answer1 is None:
                    answer1 = y * (y + 1) // 2
                else:
                    answer1 = max(answer1, y * (y + 1) // 2)
                answer2 += 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 17, solve_puzzle)


if __name__ == '__main__':
    main()
