import config


class Ship:
    __sz = int
    __environment = set()
    __coordinates = [(int, int)]

    def __init__(self, coordinates):
        self.__coordinates = coordinates
        self.__sz = len(coordinates)

        self.__environment.clear()
        for x, y in self.__coordinates:
            for counter in range(9):
                if (0 <= x + counter % 3 - 1 < config.row) and (0 <= y + counter // 3 - 1 < config.column):
                    self.__environment.add((x + counter % 3 - 1, y + counter // 3 - 1))
        self.__environment = self.__environment.difference(set(self.__coordinates))

    def shot(self):
        self.__sz -= 1
        if self.__sz != 0:
            # ранил
            return {}
        # убил
        return self.get_environment()

    def get_environment(self):
        return self.__environment
