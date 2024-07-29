from random import randint

import config
from battlefield import Battlefield


class BattlefieldBotPlayer(Battlefield):

    def take_a_shot(self):
        probability_field = []
        probability_field_only_hit = []
        constant_to_drop_fields_only_hit = 10
        # needed to make the bot hit more often
        for x in range(config.COLUMN):
            for y in range(config.ROW):
                if not isinstance(self._field[y][x], str):
                    probability_field.append((x, y))
                if not isinstance(self._field[y][x], (str, int)):
                    probability_field_only_hit.append((x, y))
        index = randint(0, (len(probability_field) + constant_to_drop_fields_only_hit))
        self._existence_of_raw_shot = False
        if index >= len(probability_field):
            index = randint(0, (len(probability_field_only_hit) - 1))
            self._shot(*probability_field_only_hit[index])
            return
        self._shot(*probability_field[index])
