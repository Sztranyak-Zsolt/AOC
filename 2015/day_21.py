from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CItem:
    def __init__(self, p_name, p_cost, p_damage, p_armor, p_type):
        self.name = p_name
        self.type = p_type
        self.cost = p_cost
        self.damage = p_damage
        self.armor = p_armor

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class CItemShop:
    def __init__(self):
        self.item_list: list[CItem] = list()

    def add_item(self, new_item):
        self.item_list.append(new_item)

    def yield_equipment(self):
        for weapon in [w for w in self.item_list if w.type == "Weapon"]:
            for armor in [w for w in self.item_list if w.type == "Armor"]:
                for ring_rank1, ring1 in [(i, w) for i, w in enumerate(self.item_list) if w.type == "Ring"]:
                    for ring_rank2, ring2 in [(i, w) for i, w in enumerate(self.item_list) if w.type == "Ring"]:
                        if ring2.name == 'No_ring' or ring_rank1 < ring_rank2:
                            yield [weapon, armor, ring1, ring2]


class CPlayer:
    def __init__(self, p_name, p_init_hp, p_init_damage, p_init_armor):
        self.name = p_name
        self.init_hp = p_init_hp
        self.init_damage = p_init_damage
        self.init_armor = p_init_armor
        self.equipment_list: list[CItem] = []
        self.hp_lost = 0

    @property
    def act_damage(self):
        return self.init_damage + sum([item.damage for item in self.equipment_list])

    @property
    def act_armor(self):
        return self.init_armor + sum([item.armor for item in self.equipment_list])

    @property
    def equipment_cost(self):
        return sum([item.cost for item in self.equipment_list])


def calc_damage(att_damage, def_armor) -> int:
    if att_damage <= def_armor:
        return 1
    else:
        return att_damage - def_armor


def turns_needed_to_defeat(p_attacker: CPlayer, p_defender: CPlayer) -> int:
    if p_attacker.act_damage - p_defender.act_armor <= 1:
        return p_defender.init_hp
    else:
        turn_needed = p_defender.init_hp // (p_attacker.act_damage - p_defender.act_armor)
        if p_defender.init_hp % (p_attacker.act_damage - p_defender.act_armor) != 0:
            turn_needed += 1
        return turn_needed


def player1_win(p_player1: CPlayer, p_player2: CPlayer):
    return turns_needed_to_defeat(p_player1, p_player2) <= turns_needed_to_defeat(p_player2, p_player1)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):
    answer1 = 999999999
    answer2 = 0
    input_iter = iter(yield_input_data(p_input_file_path))
    me = CPlayer("Me", 100, 0, 0)
    boss = CPlayer("BOSS", next(input_iter)[-1], next(input_iter)[-1], next(input_iter)[-1])
    shop = CItemShop()

    for name, cost, damage, armor, item_type in yield_input_data('input/input_201521_items.txt'):
        shop.add_item(CItem(name, cost, damage, armor, item_type))
    shop.add_item(CItem("No_armor", 0, 0, 0, "Armor"))
    shop.add_item(CItem("No_ring", 0, 0, 0, "Ring"))

    for act_equipment in shop.yield_equipment():
        me.equipment_list = act_equipment
        if player1_win(me, boss):
            answer1 = min(answer1, me.equipment_cost)
        else:
            answer2 = max(answer2, me.equipment_cost)

    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 21, solve_puzzle)


if __name__ == '__main__':
    main()
