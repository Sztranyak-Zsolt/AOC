from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, neighbor_positions, add_positions


class CGrid(CGridBase):

    def is_visible(self, p_position: tuple[int, int]):
        act_height = self.position_dict[p_position]
        for direction in neighbor_positions():
            next_position = add_positions(p_position, direction)
            while True:
                if next_position not in self.position_dict:
                    return True
                if self.position_dict[next_position] >= act_height:
                    break
                next_position = add_positions(next_position, direction)
        return False

    @property
    def visible_trees_count(self):
        return len([t for t in self.position_dict if self.is_visible(t)])

    def get_direction_height_lesser(self, p_position: Position2D, p_direction: Position2D,
                                    p_height: int | None = None) -> int:
        if p_height is None:
            p_height = self.position_dict[p_position]
        new_position = Position2D(p_position.x + p_direction.x, p_position.y + p_direction.y)
        if new_position not in self.position_dict:
            return 0
        elif self.position_dict[new_position] >= p_height:
            return 1
        return 1 + self.get_direction_height_lesser(new_position, p_direction, p_height)

    def get_scenic_score(self, p_position: Position2D) -> int:
        return_score = 1
        for direction in neighbor_positions():
            return_score *= self.get_direction_height_lesser(p_position, direction)
        return return_score

    @property
    def max_scenic_score(self):
        if self.position_dict:
            return max([self.get_scenic_score(p) for p in self.position_dict])
        return None


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    g = CGrid()
    for y, inp_row in enumerate(yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False)):
        for x, h in enumerate(inp_row):
            g.add_item(Position2D(x, y), int(h))
    answer1 = g.visible_trees_count
    answer2 = g.max_scenic_score

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 8, solve_puzzle)


if __name__ == '__main__':
    main()
