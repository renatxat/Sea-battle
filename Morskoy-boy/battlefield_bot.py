import config
from battlefield import Battlefield
from random import randint


class BattlefieldBotPlayer(Battlefield):

    def __init__(self, real_field):
        super().__init__(real_field)

    def take_a_shot(self):
        probability_field = []
        probability_field_only_hit = []
        for x in range(config.row):
            for y in range(config.column):
                if not isinstance(self._field[x][y], str):
                    probability_field.append((x, y))
                if not isinstance(self._field[x][y], (str, int)):
                    probability_field_only_hit.append((x, y))
        index = randint(0, (len(probability_field) + 8))
        if index >= len(probability_field):
            index = randint(0, (len(probability_field_only_hit) - 1))
            self._shot(*probability_field_only_hit[index])
            return
        x, y = probability_field[index]
        probability_field[index], probability_field[-1] = \
            probability_field[-1], probability_field[index]
        probability_field.pop()
        self._existence_of_raw_shot = False
        self._shot(x, y)
