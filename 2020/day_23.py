from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_loop import CLoopHandlerWithKey


class CCup(CLoopHandlerWithKey):
    def move(self):
        chosen_cups = [self.act_item.right_node, self.act_item.right_node.right_node,
                       self.act_item.right_node.right_node.right_node]
        after_to_cup_index = (self.act_item.value - 2) % self.loop_size + 1
        while after_to_cup_index in [chosen_cups[0].value, chosen_cups[1].value, chosen_cups[2].value]:
            after_to_cup_index = (after_to_cup_index - 2) % self.loop_size + 1

        after_to_cup = self.loop_dict[after_to_cup_index]
        after_to_cup_next = after_to_cup.right_node

        next_cup = chosen_cups[-1].right_node
        self.act_item.right_node = next_cup
        next_cup.left_node = self.act_item

        chosen_cups[0].left_node = after_to_cup
        after_to_cup.right_node = chosen_cups[0]

        chosen_cups[-1].right_node = after_to_cup_next
        after_to_cup_next.left_node = chosen_cups[-1]

        self.move_right(1)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = ''
    input_num = next(yield_input_data(p_input_file_path, p_whole_row=True, p_convert_to_num=False), None)
    cc = CCup()
    cc2 = CCup()
    for act_cup in input_num:
        cc.add_loop_item_to_left_by_key(int(act_cup))
        cc2.add_loop_item_to_left_by_key(int(act_cup))

    for _ in range(100):
        cc.move()

    act_node = cc.loop_dict[1]
    for _ in range(8):
        act_node = act_node.right_node
        answer1 += str(act_node.value)

    for next_num in range(10, 1000001):
        cc2.add_loop_item_to_left_by_key(next_num)

    for _ in range(10000000):
        cc2.move()
    answer2 = cc2.loop_dict[1].right_node.value * cc2.loop_dict[1].right_node.right_node.value

    return answer1, answer2


def main():
    aoc_solve_puzzle(2020, 23, solve_puzzle)


if __name__ == '__main__':
    main()
