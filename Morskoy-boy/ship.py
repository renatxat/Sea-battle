import config

from itertools import product


class Ship:
    __sz = int
    __environment = set()
    __coordinates = [(int, int)]

    def __init__(self, coordinates):
        self.__coordinates = coordinates
        self.__sz = len(coordinates)

        self.__environment.clear()
        for x, y in self.__coordinates:
            env_x = [x - 1, x, x + 1]
            env_y = [y - 1, y, y + 1]
            for nearby_x, nearby_y in product(env_x, env_y):
                if 0 <= nearby_x < config.column and 0 <= nearby_y < config.row:
                    self.__environment.add((nearby_x, nearby_y))
        self.__environment = self.__environment.difference(set(self.__coordinates))

    def shot(self):
        self.__sz -= 1
        if self.__sz != 0:
            # wounded
            return {}
        # killed
        return self.get_environment()

    def get_environment(self):
        return self.__environment
