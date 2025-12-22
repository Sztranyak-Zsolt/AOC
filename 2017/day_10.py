from __future__ import annotations
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from GENERICS.aoc_loader import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_loop import CLoopItem
from typing import Self


class CLoopItemRev(CLoopItem):
    def __init__(self, p_value: int):
        super().__init__(p_value)
        self.reversed = False

    def get_act_left(self) -> Self:
        return self.left_node if not self.reversed else self.right_node

    def get_act_right(self) -> Self:
        return self.right_node if not self.reversed else self.left_node

    def set_act_left(self, p_li: Self):
        if not self.reversed:
            self.left_node = p_li
        else:
            self.right_node = p_li

    def set_act_right(self, p_li: Self):
        if not self.reversed:
            self.right_node = p_li
        else:
            self.left_node = p_li


class CKnotHash:
    def __init__(self, p_loop_size: int):
        self.loop_size = p_loop_size
        self.first_item = CLoopItemRev(0)
        self.act_item = self.first_item
        self.skip_size = 0
        for li in range(1, p_loop_size):
            self.first_item.add_node_to_left(CLoopItemRev(li))

    def reverse_nodes(self, p_length: int):
        nodes_to_reverse = list([self.act_item])
        for _ in range(1, p_length):
            nodes_to_reverse.append(nodes_to_reverse[-1].get_act_right())
        prev_node, next_node = nodes_to_reverse[0].get_act_left(), nodes_to_reverse[-1].get_act_right()
        for n in nodes_to_reverse:
            n.reversed = not n.reversed
        if self.first_item in nodes_to_reverse:
            self.first_item = nodes_to_reverse[-1-nodes_to_reverse.index(self.first_item)]
        self.act_item = nodes_to_reverse[-1]
        if len(nodes_to_reverse) == self.loop_size:
            return
        prev_node.set_act_right(nodes_to_reverse[-1])
        next_node.set_act_left(nodes_to_reverse[0])
        nodes_to_reverse[0].set_act_right(next_node)
        nodes_to_reverse[-1].set_act_left(prev_node)

    def move_position(self, p_move_step: int):
        for _ in range(p_move_step):
            self.act_item = self.act_item.get_act_right()
        self.skip_size += 1

    def operate(self, p_length: int):
        if p_length > 1:
            self.reverse_nodes(p_length)
        self.move_position(p_length + self.skip_size)

    @property
    def dense_hash_hex(self):
        rl = [0] * 16
        act_item = self.first_item
        for i in range(256):
            rl[i // 16] ^= act_item.value
            act_item = act_item.get_act_right()
        return ''.join([f"{x:#04x}".replace('0x', '') for x in rl])

    @property
    def dense_hash_bit(self):
        rl = [0] * 16
        act_item = self.first_item
        for i in range(256):
            rl[i // 16] ^= act_item.value
            act_item = act_item.get_act_right()
        return ''.join([f"{x:#010b}".replace('0b', '') for x in rl])

    def create_hash(self, p_length: str | list[int]):
        if isinstance(p_length, str):
            p_length = [ord(c) for c in p_length]
        for _ in range(64):
            for act_l in p_length + [17, 31, 73, 47, 23]:
                self.operate(act_l)

    def __str__(self):
        if self.first_item == self.act_item:
            ret_str = f'[{self.first_item.value}]'
        else:
            ret_str = str(self.first_item.value)
        curr_item = self.first_item.get_act_right()
        while curr_item != self.first_item:
            if curr_item == self.act_item:
                ret_str += f' [{curr_item.value}]'
            else:
                ret_str += f' {curr_item.value}'
            curr_item = curr_item.get_act_right()
        return ret_str


def solve_puzzle(p_input_file_path: str) -> tuple[int | str, int | str | None]:
    length_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)
    kh = CKnotHash(256)
    for act_l in length_list:
        kh.operate(act_l)
    answer1 = kh.first_item.value * kh.first_item.get_act_right().value

    kh = CKnotHash(256)
    kh.create_hash(next(yield_input_data(p_input_file_path, p_whole_row=True), None))
    answer2 = kh.dense_hash_hex
    return answer1, answer2


def main():
    aoc_solve_puzzle(2017, 10, solve_puzzle)


if __name__ == '__main__':
    main()
