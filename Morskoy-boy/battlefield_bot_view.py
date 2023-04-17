from battlefield_opponent_view import BattlefieldOpponent
import config
from random import randint
from ship import Ship


class BattlefieldBotOpponent(BattlefieldOpponent):

    def __init__(self, canvas):
        probability_field = [(x, y) for x in range(config.row) for y in range(config.column)]
        self.dict_index_elem = {(x, y): x * config.column + y for x in range(config.row) for y in range(config.column)}
        real_field = [[0 for _ in range(config.column)] for _ in range(config.row)]
        number_ships = 0
        while number_ships != len(config.ship_sizes):
            while True:
                size = config.ship_sizes[number_ships]
                index = randint(0, len(probability_field) - 1)
                x, y = probability_field[index]
                vertical = randint(0, 1)
                if self.check_ship(size, vertical, x, y):
                    number_ships += 1
                    ship = []
                    for _ in range(size):
                        ship.append((x, y))
                        x, y = x + vertical, y + 1 - vertical
                    real_ship = Ship(ship)
                    print(ship)
                    for (x, y) in ship:
                        index = self.dict_index_elem[(x, y)]
                        if index == -2:
                            self.dict_index_elem[(x, y)] = -1
                        else:
                            self.dict_index_elem[probability_field[-1]] = index
                            self.dict_index_elem[probability_field[index]] = -1
                            # -1 means that a ship is located on the cell

                            probability_field[index], probability_field[-1] = \
                                probability_field[-1], probability_field[index]
                            probability_field.pop()
                            real_field[x][y] = real_ship

                    environment = real_ship.get_environment()
                    for (x, y) in environment:
                        index = self.dict_index_elem[(x, y)]
                        if index != -2:
                            self.dict_index_elem[probability_field[-1]] = index
                            self.dict_index_elem[probability_field[index]] = -2
                            # -2 means that the unsuitable cells from environment ships

                            probability_field[index], probability_field[-1] = \
                                probability_field[-1], probability_field[index]
                            probability_field.pop()
                    break

        super().__init__(real_field, canvas)

    def check_ship(self, size, vertical, x, y):
        ship_and_environment = []

        for _ in range(size):
            if not (0 <= x < config.row and 0 <= y < config.column):
                return False
            for counter in range(9):
                ship_and_environment.append((x + counter % 3 - 1, y + counter // 3 - 1))
            x, y = x + vertical, y + 1 - vertical

        for (x, y) in ship_and_environment:
            if 0 <= x < config.row and 0 <= y < config.column and self.dict_index_elem[(x, y)] == -1:
                return False
        return True
