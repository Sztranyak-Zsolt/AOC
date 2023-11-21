from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import CGridBase
from GENERICS.aoc_vector import Position2D, neighbor_positions, add_positions


class CElf:
    def __init__(self, p_repr_str: str):
        self.proposed_position: Position2D | None = None
        self.repr_str = p_repr_str

    def __str__(self):
        return self.repr_str


class CGrid(CGridBase):
    prop_dir = [(Position2D(0, 1), (Position2D(-1, 1), Position2D(0, 1), Position2D(1, 1))),
                (Position2D(0, -1), (Position2D(-1, -1), Position2D(0, -1), Position2D(1, -1))),
                (Position2D(-1, 0), (Position2D(-1, -1), Position2D(-1, 0), Position2D(-1, 1))),
                (Position2D(1, 0), (Position2D(1, -1), Position2D(1, 0), Position2D(1, 1)))]

    def __init__(self):
        super().__init__()
        self.position_dict: dict[Position2D, CElf] = {}
        self.elves_list: list[CElf] = list()
        self.act_facing = 0

    def make_proposals(self):
        for act_elf_pos, act_elf in self.position_dict.items():
            for np in neighbor_positions(act_elf_pos, p_return_corner=True):
                if np in self.position_dict:
                    break
            else:
                continue
            for f_plus in range(4):
                act_elf_facing = (self.act_facing + f_plus) % 4
                prop_dir, dirs_to_check = self.prop_dir[act_elf_facing]
                for dir_to_check in dirs_to_check:
                    if add_positions(act_elf_pos, dir_to_check) in self.position_dict:
                        break
                else:
                    self.position_dict[act_elf_pos].proposed_position = add_positions(act_elf_pos, prop_dir)
                    break

    def make_steps(self):
        has_step = False
        valid_proposals = {None: False}
        for act_elf in self.position_dict.values():
            if act_elf.proposed_position in valid_proposals:
                valid_proposals[act_elf.proposed_position] = False
                continue
            valid_proposals[act_elf.proposed_position] = True
        for act_elf_pos, act_elf in list(self.position_dict.items()):
            if act_elf.proposed_position is not None and valid_proposals[act_elf.proposed_position]:
                self.position_dict[act_elf.proposed_position] = act_elf
                del self.position_dict[act_elf_pos]
                has_step = True
            act_elf.proposed_position = None
        self.min_x = min([p.x for p in self.position_dict])
        self.max_x = max([p.x for p in self.position_dict])
        self.min_y = min([p.y for p in self.position_dict])
        self.max_y = max([p.y for p in self.position_dict])
        return has_step

    def evolve_grid(self):
        self.make_proposals()
        self.act_facing = (self.act_facing + 1) % 4
        return self.make_steps()


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = None
    g = CGrid()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True, p_reversed=True):
        g.add_row(inp_row, p_chars_to_skip='.', p_item_type=CElf)

    c = 0
    while g.evolve_grid():
        c += 1
        if c == 10:
            answer1 = (g.max_x - g.min_x + 1) * (g.max_y - g.min_y + 1) - len(g.position_dict)
    answer2 = c + 1

    return answer1, answer2


def main():
    aoc_solve_puzzle(2022, 23, solve_puzzle)


if __name__ == '__main__':
    main()
