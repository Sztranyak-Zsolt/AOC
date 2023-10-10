from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle


class CReindeer:
    def __init__(self, p_reindeer_name, p_speed, p_fly_time, p_rest_time):
        self.reindeer_name = p_reindeer_name
        self.speed = p_speed
        self.fly_time = p_fly_time
        self.rest_time = p_rest_time

    def calc_distance(self, p_time: int) -> int:
        period = self.fly_time + self.rest_time
        round_count = p_time // period
        remaining_time = p_time % period
        return self.speed * (round_count * self.fly_time + min(remaining_time, self.fly_time))


class CReindeerHandler:
    def __init__(self):
        self.rd_list: list[CReindeer] = list()

    def calc_max_distance(self, p_time) -> int:
        return max([rd.calc_distance(p_time) for rd in self.rd_list])

    def calc_scores(self, p_time) -> int:
        rd_score: dict[CReindeer, int] = {}
        for act_time in range(1, p_time + 1):
            act_max_dist = self.calc_max_distance(act_time)
            for act_rd in self.rd_list:
                if act_rd.calc_distance(act_time) == act_max_dist:
                    rd_score[act_rd] = rd_score.get(act_rd, 0) + 1
        return max(rd_score.values())


def solve_puzzle(p_input_file_path: str) -> (int, int):
    fly_time = 2503
    rh = CReindeerHandler()
    for reindeer_name, _, _, rd_speed, _, _, rd_fly_time, *_, rd_rest_time, _ in yield_input_data(p_input_file_path):
        rh.rd_list.append(CReindeer(reindeer_name, rd_speed, rd_fly_time, rd_rest_time))
    answer1 = rh.calc_max_distance(fly_time)
    answer2 = rh.calc_scores(fly_time)
    return answer1, answer2


def main():
    aoc_solve_puzzle(2015, 14, solve_puzzle)


if __name__ == '__main__':
    main()
