from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


def reallocate_memory(p_memory: list[int]):
    mem_to_allocate = max(p_memory)
    act_mem_index = p_memory.index(mem_to_allocate)
    p_memory[act_mem_index] = 0
    while mem_to_allocate != 0:
        act_mem_index += 1
        p_memory[act_mem_index % len(p_memory)] += 1
        mem_to_allocate -= 1


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = 0
    inp_list = next(yield_input_data(p_input_file_path), None)

    inp_cache = []
    while tuple(inp_list) not in inp_cache:
        answer1 += 1
        inp_cache.append(tuple(inp_list))
        reallocate_memory(inp_list)
    answer2 = len(inp_cache) - inp_cache.index(tuple(inp_list))

    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 6, solve_puzzle)


if __name__ == '__main__':
    main()
