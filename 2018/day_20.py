from __future__ import annotations
from GENERICS.aoc2 import yield_input_data, aoc_solve_puzzle
from GENERICS.aoc_grid import Position2D, add_positions
from functools import cached_property
from collections import deque


def calc_pos(p_pos: Position2D, p_dir: str) -> Position2D:
    if p_dir == 'W':
        return Position2D(p_pos.x - 1, p_pos.y)
    elif p_dir == 'E':
        return Position2D(p_pos.x + 1, p_pos.y)
    elif p_dir == 'N':
        return Position2D(p_pos.x, p_pos.y + 1)
    elif p_dir == 'S':
        return Position2D(p_pos.x, p_pos.y - 1)


class CRoom:
    def __init__(self):
        self.doors: list[Position2D] = []


class CMaze:
    def __init__(self, p_maze_str: str | list[str]):
        self.starting_position = Position2D(0, 0)
        self.rooms: dict[Position2D, CRoom] = {self.starting_position: CRoom()}
        if isinstance(p_maze_str, str):
            p_maze_str = list(p_maze_str)
        if p_maze_str[0] == '^':
            p_maze_str.pop(0)
        self.set_maze(p_maze_str)

    def set_maze(self, p_maze_list: list[str], p_starting_position_set: set[Position2D] | None = None):
        if p_starting_position_set is None:
            p_starting_position_set = {self.starting_position}
        act_position_list: list[Position2D] = list(p_starting_position_set)
        end_position_set = set()
        while p_maze_list:
            next_position_list = []
            act_str = p_maze_list.pop(0)
            if act_str in (')', '$'):
                return list(end_position_set | set(act_position_list))
            elif act_str == '(':
                act_position_list = self.set_maze(p_maze_list, set(act_position_list))
            elif act_str == '|':
                end_position_set |= set(act_position_list)
                act_position_list = list(p_starting_position_set)
            elif act_str in 'NSEW':
                for act_position in act_position_list:
                    act_room = self.rooms[act_position]
                    next_position = calc_pos(act_position, act_str)
                    next_dir = calc_pos(Position2D(0, 0), act_str)
                    if next_position not in self.rooms:
                        self.rooms[next_position] = CRoom()
                    act_room.doors.append(next_dir)
                    self.rooms[next_position].doors.append(Position2D(-next_dir.x, -next_dir.y))
                    next_position_list.append(next_position)
                act_position_list = next_position_list

    @cached_property
    def room_distance_dict(self) -> dict[Position2D, int]:
        rd = {self.starting_position: 0}
        dq = deque([self.starting_position])
        while dq:
            act_position = dq.popleft()
            next_step = rd[act_position] + 1
            for next_room_dir in self.rooms[act_position].doors:
                next_pos = add_positions(act_position, next_room_dir)
                if next_pos not in rd:
                    rd[next_pos] = next_step
                    dq.append(next_pos)
        return rd

    def __str__(self):
        rv_list = list()
        min_x = min([p.x for p in self.rooms])
        max_x = max([p.x for p in self.rooms])
        min_y = min([p.y for p in self.rooms])
        max_y = max([p.y for p in self.rooms])
        rv_list.append("#" * ((max_x - min_x + 1) * 2 + 1))
        for y in range(max_y, min_y - 1, -1):
            room_str, door_str = '#', '#'
            for x in range(min_x, max_x + 1):
                if (x, y) in self.rooms:
                    if (x, y) == (0, 0):
                        room_str += "O"
                    else:
                        room_str += "."
                    if Position2D(1, 0) in self.rooms[(x, y)].doors:
                        room_str += "|"
                    else:
                        room_str += "#"
                    if Position2D(0, -1) in self.rooms[(x, y)].doors:
                        door_str += "-#"
                    else:
                        door_str += "##"
            rv_list.append(room_str)
            rv_list.append(door_str)
        return '\n'.join(rv_list)


def solve_puzzle(p_input_file_path: str) -> (int | str, int | str | None):

    maze_str = next(yield_input_data(p_input_file_path, p_whole_row=True), None)
    maze = CMaze(maze_str)

    answer1 = max(maze.room_distance_dict.values())
    answer2 = len([rd for rd in maze.room_distance_dict.values() if rd >= 1000])

    return answer1, answer2


def main():
    aoc_solve_puzzle(2018, 20, solve_puzzle)


if __name__ == '__main__':
    main()
