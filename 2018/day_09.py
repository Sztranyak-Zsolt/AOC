from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_loop import CLoopHandler


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = None
    player_count, marble_count = next(yield_input_data(p_input_file_path, p_only_nums=True), None)
    lh = CLoopHandler()
    lh.add_loop_item_to_right(0)
    act_points = [0] * player_count
    for i in range(1, marble_count * 100 + 1):
        if i % 23 == 0:
            lh.move_left(7)
            act_points[i % len(act_points)] += i + lh.pop_act_loop_item().value
        else:
            lh.move_right(1)
            lh.act_item = lh.add_loop_item_to_right(i)
        if i == marble_count:
            answer1 = max(act_points)
    answer2 = max(act_points)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 9, solve_puzzle)


if __name__ == '__main__':
    main()
