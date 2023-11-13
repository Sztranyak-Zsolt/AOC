from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import CVector2D
from collections import namedtuple


ChartState = namedtuple('ChartState', ['act_direction', 'act_to_turn'])


class CGridX(CGridBase):
    direction_list = [CVector2D(1, 0), CVector2D(0, 1), CVector2D(-1, 0), CVector2D(0, -1)]
    turn_dict = {(0, "\\"): 1, (0, "/"): 3,
                 (2, "\\"): 3, (2, "/"): 1,
                 (1, "\\"): 0, (1, "/"): 2,
                 (3, "\\"): 2, (3, "/"): 0}

    def __init__(self):
        super().__init__()
        self.chart_dict: dict[CVector2D, ChartState] = {}

    def move_charts(self) -> list[CVector2D]:

        act_chart_dict = self.chart_dict.copy()
        crash_list: list[CVector2D] = []

        for act_position, act_chart_state in sorted(act_chart_dict.items(), key=lambda k: (k[0][1], k[0][0])):
            if act_position in crash_list:
                continue
            del self.chart_dict[act_position]
            new_position = act_position + self.direction_list[act_chart_state.act_direction]
            next_to_turn = act_chart_state.act_to_turn
            if self.position_dict[new_position] in ('\\', '/'):
                next_direction = self.turn_dict[(act_chart_state.act_direction, self.position_dict[new_position])]
            elif self.position_dict[new_position] == '+':
                next_direction = (act_chart_state.act_direction + act_chart_state.act_to_turn) % 4
                next_to_turn += 1
                if next_to_turn == 2:
                    next_to_turn = -1
            else:
                next_direction = act_chart_state.act_direction
            if new_position in crash_list:
                continue
            if new_position in self.chart_dict:
                del self.chart_dict[new_position]
                crash_list.append(new_position)
            else:
                self.chart_dict[new_position] = ChartState(next_direction, next_to_turn)
        return crash_list

    def __str__(self):
        ret_lst = list()
        c_length = 2 if self.double_width_on_print else 1
        yr = slice(None) if not self.print_y_reverse else slice(None, None, -1)
        for y in range(self.max_y, self.min_y - 1, -1)[yr]:
            act_row = ''
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.chart_dict:
                    act_row += f"{'>v<^'[self.chart_dict[CVector2D(x, y)][0]]}@"[0] * c_length
                elif (x, y) in self.position_dict:
                    act_row += f"{self.position_dict[CVector2D(x, y)]}@"[0] * c_length
                else:
                    act_row += ' ' * c_length
            ret_lst.append(act_row)
        return '\n'.join(ret_lst)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = None

    g = CGridX()
    g.print_y_reverse = True
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        g.add_row(inp_row.replace('<', '-').replace('>', '-').replace('^', '|').replace('v', '|'))
        if set('>^<v') & set(inp_row):
            for x, ch in enumerate(inp_row):
                if ch in '>^<v':
                    g.chart_dict[CVector2D(x, g.max_y)] = ChartState('>v<^'.index(ch), -1)

    while len(g.chart_dict) != 1:
        next_crashes = g.move_charts()
        if answer1 is None and next_crashes != []:
            answer1 = f'{next_crashes[0].x},{next_crashes[0].y}'
    last_chart_position = list(g.chart_dict)[0]
    answer2 = f'{last_chart_position.x},{last_chart_position.y}'

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 13, solve_puzzle)


if __name__ == '__main__':
    main()
