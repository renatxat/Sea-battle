import config
from battlefield import Battlefield
from random import randint


class BattlefieldBotPlayer(Battlefield):

    def __init__(self, real_field):
        super().__init__(real_field)

    def take_a_shot(self):
        probability_field = []
        probability_field_only_hit = []
        for x in range(config.column):
            for y in range(config.row):
                if not isinstance(self._field[y][x], str):
                    probability_field.append((x, y))
                if not isinstance(self._field[y][x], (str, int)):
                    probability_field_only_hit.append((x, y))
        index = randint(0, (len(probability_field) + 13))
        self._existence_of_raw_shot = False
        if index >= len(probability_field):
            index = randint(0, (len(probability_field_only_hit) - 1))
            self._shot(*probability_field_only_hit[index])
            return
        self._shot(*probability_field[index])
