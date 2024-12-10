from __future__ import annotations
from functools import cached_property
from typing import Self, Iterator
from collections import deque


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
    def count_all_children(self):
        return len(self.child_list) + sum([x.count_all_children for x in self.child_list] + [0])

    @property
    def is_value_balanced(self) -> bool:
        return len(set([x.sum_values for x in self.child_list])) <= 1

    def add_child(self, p_child: Self):
        self.child_list.append(p_child)
        p_child.parent_item = self

    def yield_parents(self) -> Iterator[Self]:
        act_parent = self.parent_item
        while act_parent:
            yield act_parent
            act_parent = act_parent.parent_item

    def yield_all_item(self):
        for ln in self.child_list:
            for lni in ln.yield_all_item():
                yield lni
        yield self

    def yield_children(self):
        dq = deque(self.child_list)
        visited = set(self.child_list)
        while dq:
            act_child = dq.popleft()
            yield act_child
            for next_child in act_child.child_list:
                if next_child not in visited:
                    visited.add(next_child)
                    dq.append(next_child)

    def __hash__(self):
        return hash((self.name, self.value))

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value


class CTreeHandler:
    def __init__(self):
        self.node_dict: dict[str, CTreeNode] = {}
        self.act_item: CTreeNode | None = None

    def get_tree_node(self, p_node_id: str) -> CTreeNode:
        if p_node_id not in self.node_dict:
            self.node_dict[p_node_id] = CTreeNode(p_node_id)
        return self.node_dict[p_node_id]
