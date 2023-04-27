from battlefield_opponent_view import BattlefieldOpponent
from ship import Ship
import config

from random import randint
from itertools import product
from time import time


class BattlefieldBotOpponent(BattlefieldOpponent):
    __probability_field = [(int, int)]
    __dict_index_elem = {(int, int): int}
    __canvas = ["tk.Canvas()"]

    def __init__(self, canvas):
        self.__canvas = canvas
        self.__probability_field = [(x, y) for x in range(config.COLUMN) for y in range(config.ROW)]
        self.__dict_index_elem = {(x, y): x * config.ROW + y for x in range(config.COLUMN) for y in range(config.ROW)}
        self.real_field = [[0 for _ in range(config.COLUMN)] for _ in range(config.ROW)]
        self.__arrange_the_ships()
        super().__init__(self.real_field, self.__canvas)

    def __arrange_the_ships(self):
        number_ships = 0
        start_time = time()
        while number_ships != len(config.SHIP_SIZES):
            wait_constant = 10
            if time() - start_time > wait_constant:
                self.__init__(self.__canvas)

            size = config.SHIP_SIZES[number_ships]
            index = randint(0, len(self.__probability_field) - 1)
            x, y = self.__probability_field[index]
            vertical = randint(0, 1)

            if self.__check_ship(size, vertical, x, y):
                number_ships += 1
                ship = []
                for _ in range(size):
                    ship.append((x, y))
                    x, y = x + vertical, y + 1 - vertical
                real_ship = Ship(ship)

                for x, y in ship:
                    # -1 means that a ship is located on the cell
                    self.__remove_cell(self.__dict_index_elem[(x, y)], -1)
                    self.__dict_index_elem[(x, y)] = -1
                    self.real_field[y][x] = real_ship

                for x, y in real_ship.get_environment():
                    index = self.__dict_index_elem[(x, y)]
                    # -2 means that the unsuitable cells from environment ships
                    self.__remove_cell(index, -2)

    def __remove_cell(self, index, new_value_in_dict):
        if index >= 0:
            self.__dict_index_elem[self.__probability_field[-1]] = index
            self.__dict_index_elem[self.__probability_field[index]] = new_value_in_dict
            # swap with the last cell in __probability_field and pop last elements
            self.__probability_field[index], self.__probability_field[-1] = \
                self.__probability_field[-1], self.__probability_field[index]
            self.__probability_field.pop()

    def __check_ship(self, size, vertical, x, y):
        ship_and_environment = set()

        for _ in range(size):
            if not (0 <= x < config.COLUMN and 0 <= y < config.ROW):
                return False
            env_x = [x - 1, x, x + 1]
            env_y = [y - 1, y, y + 1]
            for nearby_x, nearby_y in product(env_x, env_y):
                ship_and_environment.add((nearby_x, nearby_y))
            x, y = x + vertical, y + 1 - vertical

        for x, y in ship_and_environment:
            if 0 <= x < config.COLUMN and 0 <= y < config.ROW and self.__dict_index_elem[(x, y)] == -1:
                return False
        return True
