from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from Intcode import CIntCode, InputError
from copy import copy
from typing import Iterator


class CIntCodeIdle(CIntCode):
    def __init__(self, p_init_memory_list: list[int] | None = None,
                 p_init_input_list: list[int] | None = None):
        super().__init__(p_init_memory_list, p_init_input_list)
        self.is_idle = False
        self.input_error_state_cache: list[str] = []

    def execute_next_instruction(self):
        try:
            super().execute_next_instruction()
        except InputError:
            if self.prog_state_code in self.input_error_state_cache:
                self.is_idle = True
            else:
                self.input_list.clear()
                self.input_list.append(-1)
                self.input_error_state_cache.append(self.prog_state_code)
            if len(self.input_error_state_cache) > 100:
                self.input_error_state_cache.pop(0)


class CNetwork:
    def __init__(self, p_network_intcode: CIntCodeIdle):
        self.NIC: dict[int, CIntCodeIdle] = {}
        for i in range(50):
            self.NIC[i] = copy(p_network_intcode)
            self.NIC[i].init_input_list = [i]
            self.NIC[i].input_list = [i]
        self.NAT_operator: list[int] = []

    @property
    def network_is_idle(self):
        return min([ic.is_idle for ic in self.NIC.values()])

    def send_message(self, p_from_port) -> Iterator[tuple[int, int, int, int]]:
        if p_from_port != 255:
            from_ic = self.NIC[p_from_port]
            to_port, value_x, value_y = from_ic.output_list.pop(0), from_ic.output_list.pop(0),\
                from_ic.output_list.pop(0)
        else:
            to_port, value_x, value_y = 0, self.NAT_operator.pop(-2), self.NAT_operator.pop(-1)
            yield 255, 0, value_x, value_y
        if to_port != 255:
            if self.NIC[to_port].input_list == [-1]:
                self.NIC[to_port].input_list.clear()
            self.NIC[to_port].input_list.extend([value_x, value_y])
            self.NIC[to_port].is_idle = False
        else:
            yield p_from_port, 255, value_x, value_y
            self.NAT_operator.extend([value_x, value_y])

    def run_network(self) -> Iterator[tuple[int, int, int, int]]:
        while True:
            while not self.network_is_idle:
                for act_nic_id in range(50):
                    act_nic = self.NIC[act_nic_id]
                    if act_nic.is_idle:
                        continue
                    act_nic.execute_next_instruction()
                    if len(act_nic.output_list) != 3:
                        continue
                    for act_send_info in self.send_message(act_nic_id):
                        yield act_send_info
            for act_send_info in self.send_message(255):
                yield act_send_info


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = None

    num_list = next(yield_input_data(p_input_file_path, p_chars_to_space=','), None)

    nw = CNetwork(CIntCodeIdle(num_list))
    prev_y_send_to_0 = None
    for sender_port, receiver_port, value_x, value_y in nw.run_network():
        if answer1 is None and receiver_port == 255:
            answer1 = value_y
        if sender_port == 255:
            if prev_y_send_to_0 is None or value_y != prev_y_send_to_0:
                prev_y_send_to_0 = value_y
                continue
            answer2 = value_y
            break

    return answer1, answer2


def main():
    aoc_solve_puzzle(2019, 23, solve_puzzle)


if __name__ == '__main__':
    main()
