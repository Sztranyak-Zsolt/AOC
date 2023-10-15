from __future__ import annotations
from typing import Self


class CLoopItem:
    def __init__(self, p_value: int | str = 0):
        self.value = p_value
        self.left_node: Self = self
        self.right_node: Self = self

    def add_node_to_left(self, p_node: Self):
        act_left = self.left_node
        p_node.left_node = act_left
        act_left.right_node = p_node
        self.left_node = p_node
        p_node.right_node = self

    def add_node_to_right(self, p_node: Self):
        act_right = self.right_node
        p_node.right_node = act_right
        act_right.left_node = p_node
        self.right_node = p_node
        p_node.left_node = self


class CLoopHandler:
    def __init__(self):
        self.act_item: CLoopItem | None = None
        self.loop_size = 0

    def add_loop_item_to_left(self, p_item_value: int | str) -> CLoopItem:
        self.loop_size += 1
        if self.act_item is None:
            self.act_item = CLoopItem(p_item_value)
        else:
            self.act_item.add_node_to_left(CLoopItem(p_item_value))
        return self.act_item.left_node

    def add_loop_item_to_right(self, p_item_value: int | str) -> CLoopItem:
        self.loop_size += 1
        if self.act_item is None:
            self.act_item = CLoopItem(p_item_value)
        else:
            self.act_item.add_node_to_right(CLoopItem(p_item_value))
        return self.act_item.right_node

    def move_left(self, p_step: int, p_check_move_step: bool = False) -> CLoopItem | None:
        if self.loop_size == 0:
            return None
        if p_step == 1:
            self.act_item = self.act_item.left_node
            return self.act_item
        if p_check_move_step:
            p_step = p_step % self.loop_size
            if p_step > self.loop_size // 2 + 1:
                return self.move_right(self.loop_size - p_step)
        for _ in range(p_step):
            self.act_item = self.act_item.left_node
        return self.act_item

    def move_right(self, p_step: int, p_check_move_step: bool = False) -> CLoopItem | None:
        if self.loop_size == 0:
            return None
        if p_step == 1:
            self.act_item = self.act_item.right_node
            return self.act_item
        if p_check_move_step:
            p_step = p_step % self.loop_size
            if p_step > self.loop_size // 2 + 1:
                return self.move_left(self.loop_size - p_step)
        for _ in range(p_step):
            self.act_item = self.act_item.right_node
        return self.act_item

    def pop_act_loop_item(self) -> CLoopItem | None:
        if self.act_item is None:
            return None
        self.loop_size -= 1
        ai = self.act_item

        if self.loop_size == 0:

            self.act_item = None
            return ai

        ln, rn = ai.left_node, ai.right_node
        ln.right_node, rn.left_node = rn, ln
        ai.left_node = ai.right_node = ai
        self.act_item = rn

        return ai

    def get_item_by_index(self, p_index: int) -> CLoopItem | None:
        if self.loop_size == 0:
            return None
        ri = self.act_item
        for _ in range(p_index % self.loop_size):
            ri = ri.right_node
        return ri

    def swap_loop_item_by_index(self, p_index1: int, p_index2: int):
        n1 = self.get_item_by_index(p_index1)
        n2 = self.get_item_by_index(p_index2)
        if n1 is not None:
            self.swap_loop_item(n1, n2)

    def swap_loop_item(self, p_node1: CLoopItem, p_node2: CLoopItem):
        if p_node1 == p_node2:
            return

        if p_node1.left_node == p_node2:
            self.swap_loop_item(p_node2, p_node1)
            return

        nl1, nr1 = p_node1.left_node, p_node1.right_node
        nl2, nr2 = p_node2.left_node, p_node2.right_node

        if self.act_item == p_node1:
            self.act_item = p_node2
        elif self.act_item == p_node2:
            self.act_item = p_node1

        nl1.right_node, p_node2.left_node = p_node2, nl1
        nr2.left_node, p_node1.right_node = p_node1, nr2

        if nr1 == p_node2:
            p_node2.right_node, p_node1.left_node = p_node1, p_node2
            return

        p_node2.right_node, nr1.left_node = nr1, p_node2
        p_node1.left_node, nl2.right_node = nl2, p_node1

    def get_list(self):
        if self.act_item is None:
            return []
        ret_list = [self.act_item.value]
        curr_item = self.act_item.right_node
        c = 0
        while curr_item != self.act_item:
            ret_list.append(curr_item.value)
            curr_item = curr_item.right_node
            c += 1
        return ret_list

    def __str__(self):
        return ' '.join([str(x) for x in self.get_list()])


class CLoopHandlerWithKey(CLoopHandler):
    def __init__(self):
        super().__init__()
        self.loop_dict: dict[int | str, CLoopItem] = {}

    def add_loop_item_to_left_by_key(self, p_key: int | str) -> CLoopItem:
        self.loop_size += 1
        if self.act_item is None:
            self.act_item = CLoopItem(p_key)
            self.loop_dict[p_key] = self.act_item
        else:
            self.act_item.add_node_to_left(CLoopItem(p_key))
            self.loop_dict[p_key] = self.act_item.left_node
        return self.loop_dict[p_key]

    def add_loop_item_to_right_by_key(self, p_key: int | str) -> CLoopItem:
        self.loop_size += 1
        if self.act_item is None:
            self.act_item = CLoopItem(p_key)
            self.loop_dict[p_key] = self.act_item
        else:
            self.act_item.add_node_to_right(CLoopItem(p_key))
            self.loop_dict[p_key] = self.act_item.right_node
        return self.loop_dict[p_key]

    def pop_act_loop_item(self) -> CLoopItem | None:
        ai = super().pop_act_loop_item()
        if ai is None:
            return None
        return self.loop_dict.pop(ai.value)

    def pop_loop_item_by_key(self, p_key: int | str) -> CLoopItem | None:
        if p_key not in self.loop_dict:
            return None
        self.loop_size -= 1
        if self.loop_size == 0:
            return self.loop_dict.pop(p_key)
        n = self.loop_dict[p_key]
        ln, rn = n.left_node, n.right_node
        ln.right_node, rn.left_node = rn, ln
        n.left_node = n.right_node = n
        return self.loop_dict.pop(p_key)

    def swap_loop_item_by_key(self, p_key1: int | str, p_key2: int | str):
        if p_key1 not in self.loop_dict or p_key2 not in self.loop_dict:
            return
        self.swap_loop_item(self.loop_dict[p_key1], self.loop_dict[p_key2])
