from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from copy import copy


class CSnailFishTree:
    def __init__(self, p_value: int = 0):
        self.left: CSnailFishTree | None = None
        self.right: CSnailFishTree | None = None
        self.parent: CSnailFishTree | None = None
        self.value = p_value

    @property
    def root(self):
        if self.parent:
            return self.parent.root()
        return self

    @property
    def level(self) -> int:
        if self.parent:
            return self.parent.level + 1
        return 0

    @property
    def is_node(self) -> bool:
        return self.left is None and self.right is None

    @property
    def magnitude(self) -> int:
        if self.is_node:
            return self.value
        return 3 * self.left.magnitude + 2 * self.right.magnitude

    def __copy__(self):
        new_instance = CSnailFishTree()
        new_instance.value = self.value
        if self.left:
            new_instance.left = copy(self.left)
            new_instance.left.parent = new_instance
        if self.right:
            new_instance.right = copy(self.right)
            new_instance.right.parent = new_instance
        return new_instance

    def __add__(self, other: CSnailFishTree) -> CSnailFishTree:
        new_sf = CSnailFishTree()
        new_sf.left = copy(self)
        new_sf.left.parent = new_sf
        new_sf.right = copy(other)
        new_sf.right.parent = new_sf
        new_sf.reduce_tree()
        return new_sf

    def yield_node_from_left(self):
        if self.is_node:
            yield self
            return
        for node in self.left.yield_node_from_left():
            yield node
        for node in self.right.yield_node_from_left():
            yield node

    def explode(self) -> bool:
        act_node_list = list(self.yield_node_from_left())
        for i, act_node in enumerate(act_node_list):
            if act_node.level == 5:
                if i != 0:
                    act_node_list[i - 1].value += act_node.parent.left.value
                if i != len(act_node_list) - 2:
                    act_node_list[i + 2].value += act_node.parent.right.value
                act_node.parent.value = 0
                act_node.parent.left = act_node.parent.right = None
                return True
        return False

    def split(self):
        for act_node in self.yield_node_from_left():
            if act_node.value >= 10 and act_node.is_node:
                act_node.left = CSnailFishTree(act_node.value // 2)
                act_node.left.parent = act_node
                act_node.right = CSnailFishTree(act_node.value - act_node.value // 2)
                act_node.right.parent = act_node
                act_node.value = 0
                return True
        return False

    def reduce_tree(self):
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            break

    def __str__(self):
        if self.is_node:
            return f'{self.value}'
        return f'[{self.left}, {self.right}]'


def create_sf_tree(p_sf_num_list: list) -> CSnailFishTree:
    part1, part2 = p_sf_num_list[0], p_sf_num_list[1]
    rsf = CSnailFishTree()
    if isinstance(part1, int):
        rsf.left = CSnailFishTree(part1)
    else:
        rsf.left = create_sf_tree(part1)
    rsf.left.parent = rsf
    if isinstance(part2, int):
        rsf.right = CSnailFishTree(part2)
    else:
        rsf.right = create_sf_tree(part2)
    rsf.right.parent = rsf
    return rsf


class CSnailFishHandler:
    def __init__(self):
        self.sf_list: list[CSnailFishTree] = []

    @property
    def sf_sum(self) -> CSnailFishTree:
        if not self.sf_list:
            return CSnailFishTree()
        act_sum = self.sf_list[0]
        for act_sf in self.sf_list[1:]:
            act_sum = act_sum + act_sf
        return act_sum

    @property
    def max_addition_magnitude(self) -> int:
        rv = 0
        for sf1 in self.sf_list:
            for sf2 in self.sf_list:
                rv = max(rv, (sf1 + sf2).magnitude)
                rv = max(rv, (sf2 + sf1).magnitude)
        return rv


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    sfh = CSnailFishHandler()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=True):
        sfh.sf_list.append(create_sf_tree(eval(inp_row)))
    answer1 = sfh.sf_sum.magnitude
    answer2 = sfh.max_addition_magnitude
    return answer1, answer2


def main():
    aoc_solve_puzzle(2021, 18, solve_puzzle)


if __name__ == '__main__':
    main()
