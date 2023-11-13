from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CDigitCoder:
    def __init__(self):
        self.decoder: dict[str, str] = {}
        self.output: str = ''

    @property
    def output_digit1478(self) -> int:
        return self.output.count('1') + self.output.count('4') + self.output.count('7') + self.output.count('8')

    @property
    def output_value(self) -> int:
        return int(self.output)

    def add_digit_list(self, p_digit_list: list[str]):
        len_decoder_dict = {2: '1', 3: '7', 4: '4', 5: None, 6: None, 7: '8'}
        for digit in p_digit_list:
            self.decoder[''.join(sorted(digit))] = len_decoder_dict[len(digit)]
        self.decode_other_digits()

    def add_output(self, p_output_list: list[str]):
        self.output = ''.join([self.decoder[''.join(sorted(s))] for s in p_output_list])

    def decode_other_digits(self):
        code_dict = {v: k for k, v in self.decoder.items() if v is not None}
        not_coded_digits = {k for k, v in self.decoder.items() if v is None}
        for act_digit in not_coded_digits:
            if len(act_digit) == 5:
                if len(set(act_digit) & set(code_dict['1'])) == 2:
                    self.decoder[act_digit] = '3'
                elif len(set(act_digit) & set(code_dict['4'])) == 2:
                    self.decoder[act_digit] = '2'
                else:
                    self.decoder[act_digit] = '5'
            else:
                if len(set(act_digit) & set(code_dict['4'])) == 4:
                    self.decoder[act_digit] = '9'
                elif len(set(act_digit) & set(code_dict['7'])) == 3:
                    self.decoder[act_digit] = '0'
                else:
                    self.decoder[act_digit] = '6'


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    for inp_row in yield_input_data(p_input_file_path, p_chars_to_space='|'):
        dc = CDigitCoder()
        dc.add_digit_list(inp_row[:10])
        dc.add_output(inp_row[10:])
        answer1 += dc.output_digit1478
        answer2 += dc.output_value
    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 8, solve_puzzle)


if __name__ == '__main__':
    main()
