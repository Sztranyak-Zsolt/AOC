from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from Intcode import CIntCode
from GENERICS.aoc_grid import CGridBase, Position2D


class CScreen(CGridBase):
    def __init__(self):
        super().__init__()
        self.print_y_reverse = True
        self.ball_position = Position2D(-1, -1)
        self.paddle_position = Position2D(-1, -1)
        self.act_point = 0


class CGame:
    def __init__(self, p_game_code: list[int]):
        self.game = CIntCode(p_game_code)
        self.screen = CScreen()

    @property
    def blocks_count(self) -> int:
        self.play_game()
        return len([b for b in self.screen.position_dict.values() if b == '#'])

    @property
    def final_score(self) -> int:
        self.play_game()
        return self.screen.act_point

    def play_game(self):
        str_dict = {0: ' ', 2: '#', 4: 'o', 3: '=', 1: 'X'}

        self.screen.act_point = 0
        self.game.reset_program()

        while True:
            if self.screen.ball_position.x < self.screen.paddle_position.x:
                self.game.input_list = [-1]
            elif self.screen.ball_position.x > self.screen.paddle_position.x:
                self.game.input_list = [1]
            else:
                self.game.input_list = [0]
            self.game.run_until_next_outputs(3)
            if self.game.program_finished:
                break
            x, y, value = self.game.output_list.pop(0), self.game.output_list.pop(0), self.game.output_list.pop(0)
            if x == -1:
                self.screen.act_point = value
                for x_i, act_v in enumerate(str(value)):
                    self.screen.add_item(Position2D(x, -1), act_v)
            else:
                self.screen.add_item(Position2D(x, y), str_dict[value])
                if value == 4:
                    if self.screen.ball_position != Position2D(-1, -1):
                        del self.screen.position_dict[self.screen.ball_position]
                    self.screen.ball_position = Position2D(x, y)
                elif value == 3:
                    if self.screen.paddle_position != Position2D(-1, -1):
                        del self.screen.position_dict[self.screen.paddle_position]
                    self.screen.paddle_position = Position2D(x, y)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    num_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)

    g = CGame(num_list)
    answer1 = g.blocks_count

    g.game.init_memory_list[0] = 2
    answer2 = g.final_score

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 13, solve_puzzle)


if __name__ == '__main__':
    main()
