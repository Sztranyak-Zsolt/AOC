from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from collections import deque
from math import lcm


class CModule:
    def __init__(self, p_id: str, p_type: str):
        self.id = p_id
        self.state = False
        self.module_type = p_type  # BC - button/broadcast, FF - FlipFlop, CO - Conjunction
        self.sender_modules: dict[CModule, bool] = {}
        self.receiver_modules: list[CModule] = []

    def transfer_pulse(self, p_high: bool, p_sender_module: CModule):
        if self.module_type == 'BC':
            return [(self, cn, p_high) for cn in self.receiver_modules]
        if self.module_type == 'FF':
            if p_high:
                return []
            self.state = not self.state
            return [(self, cn, self.state) for cn in self.receiver_modules]
        if self.module_type == 'CO':
            self.sender_modules[p_sender_module] = p_high
            return [(self, cn, not all(self.sender_modules.values())) for cn in self.receiver_modules]


class CMachine:
    def __init__(self):
        self.module_dict: dict[str, CModule] = {}

    def get_module(self, p_key: str) -> CModule:
        p_type = 'BC'
        if p_key[0] in ['%', '&']:
            p_type = {'%': 'FF', '&': 'CO'}[p_key[0]]
            p_key = p_key[1:]
        if p_key not in self.module_dict:
            self.module_dict[p_key] = CModule(p_key, p_type)
        elif p_type != 'BC':
            self.module_dict[p_key].module_type = p_type
        return self.module_dict[p_key]

    def add_module(self, p_module_id_list: list[str]):
        act_module = self.get_module(p_module_id_list[0])
        for cn in p_module_id_list[1:]:
            act_module.receiver_modules.append(self.get_module(cn))
            self.get_module(cn).sender_modules[act_module] = False

    def push_button(self) -> (int, int, set[CModule]):
        dq = deque([[[self.get_module('button'), self.get_module('broadcaster'), False]]])
        pulse_counter_dict = {False: 0, True: 0}
        modules_sending_high = set()
        while dq:
            if len(dq[0]) == 0:
                dq.popleft()
                continue
            sending_module, receiver_module, act_send = dq[0].pop(0)
            pulse_counter_dict[act_send] += 1
            if act_send:
                modules_sending_high.add(sending_module)
            dq.append(receiver_module.transfer_pulse(act_send, sending_module))
        return pulse_counter_dict[False], pulse_counter_dict[True], modules_sending_high


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = answer2 = 0
    m = CMachine()
    for inp_row in yield_input_data(p_input_file_path, p_whole_row=False, p_chars_to_space='->,'):
        m.add_module(inp_row)

    # Info for PART 2:
    #  - rx has one input module, which is also a conjunction;
    #  - if that module receives high from all input, finally rx will get low;
    #  - that module get high periodically
    #  - final result is the lowest common multiplier of these periods
    counter = high_send_sum = low_send_sum = 0
    sending_high_to_rx_periods = {srm: 0 for srm in list(m.get_module('rx').sender_modules)[0].sender_modules}
    while not answer1 or not answer2:
        counter += 1
        low_send, high_send, rhm = m.push_button()
        high_send_sum += high_send
        low_send_sum += low_send
        for rx_sender_module in rhm & {smk for smk, smv in sending_high_to_rx_periods.items() if smv == 0}:
            sending_high_to_rx_periods[rx_sender_module] = counter
            if min(sending_high_to_rx_periods.values()):
                answer2 = lcm(*sending_high_to_rx_periods.values())
        if counter == 1000:
            answer1 = high_send_sum * low_send_sum

    return answer1, answer2


def main():
    aoc_solve_puzzle(2023, 20, solve_puzzle)


if __name__ == '__main__':
    main()
