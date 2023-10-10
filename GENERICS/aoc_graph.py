from __future__ import annotations
from typing import Self


class CGraphItem:
    def __init__(self, p_value: int = 0):
        self.value = p_value
        self.connected_nodes: list[Self] = []
        self.group_head_node = self

    def get_group_head(self) -> Self:
        if self.group_head_node == self:
            return self
        self.group_head_node = self.group_head_node.get_group_head()
        return self.group_head_node

    def connect_node(self, other: Self):
        self.connected_nodes.append(other)
        other.connected_nodes.append(self)
        self.merge_graph(other)

    def merge_graph(self, other: Self):
        other.get_group_head().group_head_node = self.get_group_head()
