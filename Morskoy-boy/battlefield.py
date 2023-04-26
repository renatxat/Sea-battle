class Battlefield:
    __quantity_ships = int
    __game_run = True
    _existence_of_raw_shot = False
    __last_shot = (0, 0)
    _field = []
    __number_call_exist_hit_last_shot = 0

    def __init__(self, real_field):
        self.__quantity_ships = len(
            set([j for i in real_field for j in i])) - 1
        self._field = real_field

    def _shot(self, x, y):
        if self._existence_of_raw_shot:
            return
        self.__last_shot = (x, y)
        self._existence_of_raw_shot = True
        if not isinstance(self._field[x][y], (int, str)):
            changes = self._field[x][y].shot()
            self._field[x][y] = 'hit'
            if len(changes) > 0:
                self.__quantity_ships -= 1
            if self.__quantity_ships == 0:
                self.__game_run = False
            for (x, y) in changes:
                self._field[x][y] = 'miss'
        elif isinstance(self._field[x][y], int):
            self._field[x][y] = 'miss'

    def presence_of_changes(self):
        return self._existence_of_raw_shot

    def get_last_shot(self):
        return self.__last_shot

    def get_run(self):
        return self.__game_run

    def existence_hit_last_shot(self):
        if self._field[self.__last_shot[0]][self.__last_shot[1]] == "hit":
            self._existence_of_raw_shot = False
            self.__number_call_exist_hit_last_shot = 0
            return True

        self.__number_call_exist_hit_last_shot += 1
        if self.__number_call_exist_hit_last_shot >= 2:
            self.__number_call_exist_hit_last_shot = 0
            self._existence_of_raw_shot = False
        return False
