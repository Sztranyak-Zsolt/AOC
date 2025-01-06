from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from collections import defaultdict


def calculate_next_secret(p_secret: int) -> int:
    p_secret = ((p_secret * 64) ^ p_secret) % 16777216
    p_secret = ((p_secret // 32) ^ p_secret) % 16777216
    p_secret = ((p_secret * 2048) ^ p_secret) % 16777216
    return p_secret


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = 0
    seq_num_sum = defaultdict(lambda: 0)

    for secret_number in yield_input_data(p_input_file_path, p_whole_row=True):
        seq = []
        visited = set()
        prev_last_digit: int | None = None

        for _ in range(2000):
            secret_number = calculate_next_secret(secret_number)
            act_last_digit = secret_number % 10
            if prev_last_digit is not None:
                seq.append(act_last_digit - prev_last_digit)
                if len(seq) == 5:
                    seq.pop(0)
                if len(seq) == 4:
                    if (act_seq := tuple(seq)) not in visited:
                        visited.add(act_seq)
                        seq_num_sum[act_seq] += act_last_digit
            prev_last_digit = act_last_digit
        answer1 += secret_number
    answer2 = max(seq_num_sum.values())

    return answer1, answer2


def main():
    aoc_solve_puzzle(2024, 22, solve_puzzle)


if __name__ == '__main__':
    main()
