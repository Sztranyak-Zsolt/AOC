from typing import Any, Iterable
from functools import cached_property


class CCodeDecode:
    def __init__(self):
        self.codes_dict: dict[Any, set[Any]] = dict()
        self.decodes_dict: dict[Any, set[Any]] = dict()

    def add_code_link(self, p_code: Any, p_decodes: Iterable[Any]):
        for act_decode in p_decodes:
            if act_decode not in self.decodes_dict:
                self.decodes_dict[act_decode] = set()
        if p_code not in self.codes_dict:
            self.codes_dict[p_code] = set(p_decodes)
            for act_decode in p_decodes:
                self.decodes_dict[act_decode].add(p_code)
        else:
            decode_to_remove = self.codes_dict[p_code] - set(p_decodes)
            self.codes_dict[p_code] &= set(p_decodes)
            for act_operation in decode_to_remove:
                self.decodes_dict[act_operation].remove(p_code)

    def reduce_codes(self, p_to_code: bool) -> bool:
        if p_to_code:
            act_dict = self.codes_dict
            linked_dict = self.decodes_dict
        else:
            act_dict = self.decodes_dict
            linked_dict = self.codes_dict

        item_found = set()
        for act_item, act_item_set in act_dict.items():
            if len(act_item_set) == 1 \
                    and len(linked_dict[list(act_item_set)[0]]) != 1:
                act_linked_item = list(act_item_set)[0]
                act_dict[act_item] = {act_linked_item}
                linked_dict[act_linked_item] = {act_item}
                item_found.add(act_linked_item)
        for linked_item_to_adjust in item_found:
            for act_item, act_item_set in act_dict.items():
                if act_item not in linked_dict[linked_item_to_adjust] \
                        and linked_item_to_adjust in act_item_set:
                    act_dict[act_item].remove(linked_item_to_adjust)
        return len(item_found) != 0

    @cached_property
    def get_code_mapping(self) -> dict:
        while self.reduce_codes(True) or self.reduce_codes(False):
            pass
        rd = {}
        for k, v in self.codes_dict.items():
            if len(v) == 0:
                rd[k] = None
            elif len(v) == 1:
                rd[k] = list(v)[0]
            else:
                rd[k] = v
        return rd

    @cached_property
    def get_decode_mapping(self) -> dict:
        while self.reduce_codes(True) or self.reduce_codes(False):
            pass
        rd = {}
        for k, v in self.decodes_dict.items():
            if len(v) == 0:
                rd[k] = None
            elif len(v) == 1:
                rd[k] = list(v)[0]
            else:
                rd[k] = v
        return rd
