import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from Intcode import CIntCode
from copy import copy
from re import search, DOTALL


class CShipProgram:
    def __init__(self, p_init_program: CIntCode):
        self.init_program = p_init_program
        self.act_program = copy(p_init_program)
        self.item_list: list[str] = []

    def run_console_mode(self):
        while True:
            self.act_program.run_until_next_input_needed()
            print(self.act_program.output_text)
            self.act_program.output_list.clear()
            if self.act_program.program_finished:
                self.act_program = copy(self.init_program)
                while (answer := input("Restart game? y/n\n")) not in ['y', 'n']:
                    print('Wrong input, only y/n is accepted!')
                if answer == 'y':
                    continue
                return
            next_command = input('*** other commands: exit / reset ***\n')
            if next_command == 'exit':
                self.act_program = copy(self.init_program)
                return
            if next_command == 'reset':
                self.act_program = copy(self.init_program)
                continue
            self.act_program.set_input_from_text_list([next_command])

    def run_commands_from_batch(self, p_input_list: list[str]):
        self.act_program.run_until_next_input_needed()
        for next_command in p_input_list:
            self.act_program.output_list.clear()
            self.act_program.set_input_from_text_list([next_command])
            self.act_program.run_until_next_input_needed()

    def take_all_items_and_move_to_final_room(self):
        input_list = ['south', 'take monolith', 'east', 'take asterisk', 'west', 'north', 'west', 'take coin', 'north',
                      'east', 'take astronaut ice cream', 'west', 'south', 'east', 'north', 'north', 'take mutex',
                      'west', 'take astrolabe', 'west', 'take dehydrated water', 'west', 'take wreath', 'east', 'south',
                      'east', 'north']
        self.item_list = ['monolith', 'asterisk', 'coin', 'astronaut ice cream', 'mutex', 'astrolabe',
                          'dehydrated water', 'wreath']
        self.run_commands_from_batch(input_list)

    def yield_set_items_on_plate(self):
        for i in range(2 ** len(self.item_list)):
            command_list = []
            reset_command_list = []
            act_n = i
            act_index = 0
            while act_n != 0:
                if act_n % 2 == 1:
                    command_list.append('drop ' + self.item_list[act_index])
                    reset_command_list.append('take ' + self.item_list[act_index])
                act_n = act_n // 2
                act_index += 1
            command_list.append('north')
            yield command_list
            yield reset_command_list

    def prog_solution(self):
        self.take_all_items_and_move_to_final_room()
        item_iterator = iter(self.yield_set_items_on_plate())
        while True:
            self.run_commands_from_batch(next(item_iterator))
            if self.act_program.program_finished:
                return search(r'[0-9]+', self.act_program.output_text, DOTALL)[0]
            self.run_commands_from_batch(next(item_iterator))


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    answer2 = None
    num_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)
    sp = CShipProgram(CIntCode(num_list))
    answer1 = sp.prog_solution()

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 25, solve_puzzle)


if __name__ == '__main__':
    main()
