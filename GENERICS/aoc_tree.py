from __future__ import annotations
from functools import cached_property
from typing import Self


class CTreeNode:
    def __init__(self, p_name: str = '', p_value: int = 0):
        self.name = p_name
        self.value = p_value
        self.parent_item: Self | None = None
        self.child_list: list[Self] = list()

    @property
    def is_root(self) -> bool:
        return self.parent_item is None

    @property
    def is_leaf(self) -> bool:
        return self.child_list == []

    @cached_property
    def act_level(self):
        if self.parent_item is None:
            return 1
        else:
            return self.parent_item.act_level + 1

    @property
    def root_node(self):
        if self.parent_item is None:
            return self
        else:
            return self.parent_item.root_node

    @property
    def sum_values(self):
        return self.value + sum([x.sum_values for x in self.child_list])

    @property
    def is_value_balanced(self) -> bool:
        return len(set([x.sum_values for x in self.child_list])) <= 1

    def add_child(self, p_child: Self):
        self.child_list.append(p_child)
        p_child.parent_item = self
