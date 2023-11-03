from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_link_decoder import CCodeDecode


class CTicket:
    def __init__(self, p_values: list[int] | None = None):
        if p_values is None:
            self.values: list[int] = []
        else:
            self.values = p_values


class CTicketValidator:
    def __init__(self):
        self.validation: dict[str, list[(int, int), (int, int)]] = dict()
        self.my_ticket: CTicket = CTicket()
        self.nearby_tickets: dict[CTicket, int | None] = {}
        self.decoder = CCodeDecode()

    def set_my_ticket(self, p_my_ticket: CTicket):
        self.my_ticket = p_my_ticket
        self.adjust_decode_by_ticket(p_my_ticket)

    def add_nearby_ticket(self, p_ticket: CTicket):
        for tn in p_ticket.values:
            for period1, period2 in self.validation.values():
                if period1[0] <= tn <= period1[1] or period2[0] <= tn <= period2[1]:
                    break
            else:
                self.nearby_tickets[p_ticket] = self.nearby_tickets.get(p_ticket, 0) + tn
        if p_ticket in self.nearby_tickets:
            return
        self.nearby_tickets[p_ticket] = None
        self.adjust_decode_by_ticket(p_ticket)

    def adjust_decode_by_ticket(self, p_ticket: CTicket):
        for i, v in enumerate(p_ticket.values):
            act_field_set = set()
            for field, periods in self.validation.items():
                if periods[0][0] <= v <= periods[0][1] or periods[1][0] <= v <= periods[1][1]:
                    act_field_set.add(field)
            self.decoder.add_code_link(i, act_field_set)

    @property
    def nearby_ticket_scan_error(self):
        return sum([v for v in self.nearby_tickets.values() if v is not None])

    @property
    def get_mapping(self) -> dict[str, int]:
        return self.decoder.get_decode_mapping


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    tv = CTicketValidator()
    inp_group = list(yield_input_data(p_input_file_path, p_group_separator='\n\n', p_chars_to_space=',-:'))
    for *key_list, period1_from, period1_to, _, period2_from, period2_to in inp_group[0]:
        tv.validation[' '.join(key_list)] = [(period1_from, period1_to), (period2_from, period2_to)]
    tv.set_my_ticket(CTicket(inp_group[1][1]))
    for nt in inp_group[2][1:]:
        tv.add_nearby_ticket(CTicket(nt))
    answer1 = tv.nearby_ticket_scan_error

    answer2 = 1
    for field, i in tv.get_mapping.items():
        if field[:9] == 'departure':
            answer2 *= tv.my_ticket.values[i]
    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 16, solve_puzzle)


if __name__ == '__main__':
    main()
