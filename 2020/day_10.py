from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    jolt_list = []
    for act_jolt in yield_input_data(p_input_file_path, p_whole_row=True):
        jolt_list.append(act_jolt)

    prev_jolt = 0
    difi_counter = {1: 0, 2: 0, 3: 1}
    possibility_dict = {0: 1}

    for act_jolt in sorted(jolt_list):
        difi_counter[act_jolt - prev_jolt] += 1
        prev_jolt = act_jolt
        possibility_dict[act_jolt] = possibility_dict.get(act_jolt - 3, 0) + possibility_dict.get(act_jolt - 2, 0) \
            + possibility_dict.get(act_jolt - 1, 0)

    answer1 = difi_counter[1] * difi_counter[3]
    answer2 = possibility_dict[prev_jolt]

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 10, solve_puzzle)


if __name__ == '__main__':
    main()
