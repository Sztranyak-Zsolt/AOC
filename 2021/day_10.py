from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CChunk:
    def __init__(self):
        self.chunk_str = ''
        self.is_incomplete = False
        self.is_corrupted = False
        self.score = 0

    @property
    def chunk_str(self):
        return self._chunk_str

    @chunk_str.setter
    def chunk_str(self, p_chunk_str):
        self._chunk_str = p_chunk_str
        p_list = []
        bracket_dict = {")": "(", "]": "[", "}": "{", ">": "<"}
        bracket_point = {"(": 1, ")": 3, "[": 2, "]": 57, "{": 3, "}": 1197, "<": 4, ">": 25137}
        for act_c in p_chunk_str:
            if act_c in bracket_dict:
                if p_list is None or p_list[-1] != bracket_dict[act_c]:
                    self.is_corrupted = True
                    self.score = bracket_point[act_c]
                    return
                p_list.pop()
            else:
                p_list.append(act_c)
        if not p_list:
            return
        self.is_incomplete = True
        while p_list:
            self.score = self.score * 5 + bracket_point[p_list.pop()]


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = 0
    incomplete_scores = []
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        c = CChunk()
        c.chunk_str = inp_row
        if c.is_corrupted:
            answer1 += c.score
        elif c.is_incomplete:
            incomplete_scores.append(c.score)
    incomplete_scores.sort()
    answer2 = incomplete_scores[len(incomplete_scores) // 2]
    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 10, solve_puzzle)


if __name__ == '__main__':
    main()
