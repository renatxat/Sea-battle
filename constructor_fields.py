import tkinter as tk
from time import time
from tkinter import messagebox
from itertools import product
from random import randint

import config
from ship import Ship
from wrappers import Window
from wrappers import Button
from wrappers import Canvas


class ConstructorFields:
    """either creates a window with the placement of ships, or places them randomly"""
    __window = ["Window()"]
    __lbl = ["tk.label"]
    __buttons = []

    __ship = [(int, int)]
    __number_ships = 0

    __real_field = [["zeros and Ships"]]
    __is_ready = False
    __is_need_for_randomness = False

    __starting_time = "time()"
    __timer = 0
    __text_before_timer = str

    def __init__(self, is_need_for_randomness=False, presence_timer=False):
        if is_need_for_randomness:
            self.__is_need_for_randomness = True
            self.__real_field = AutomaticArrangements().get_field()
            self.__is_ready = True
            return
        self.__presence_timer = presence_timer
        self.__real_field = [[0 for _ in range(config.COLUMN)] for _ in range(config.ROW)]
        self.__ship = []
        self.__window = Window(is_game_field=False)
        self.__timer = config.TIME_WAITING_CONSTRUCTOR_FIELD + 1
        self.__create_creation_window()

    def __add(self, x, y):
        self.__ship.append((x, y))
        self.__buttons[y][x].config(command=0,
                                    bg="medium purple",
                                    activebackground="medium purple")

    def __create_creation_window(self):
        canvas = Canvas(self.__window, number_of_fields=1)
        for i in range(config.ROW):
            temp = []
            for j in range(config.COLUMN):
                btn = Button(canvas,
                             state="normal",
                             bg="aqua",
                             activebackground='snow',
                             width=config.SIZE_OF_CELL,
                             height=config.SIZE_OF_CELL,
                             borderwidth=1)
                temp.append(btn)
            self.__buttons.append(temp)
        for i in range(config.ROW):
            for j in range(config.COLUMN):
                self.__buttons[i][j]["command"] = lambda x=j, y=i: self.__add(x, y)
        for i in range(config.ROW):
            for j in range(config.COLUMN):
                self.__buttons[i][j].pack(expand=False, side="top")
                canvas.create_window((j * config.SIZE_OF_CELL, i * config.SIZE_OF_CELL),
                                     anchor="nw",
                                     window=self.__buttons[i][j])
        self.__text_before_timer = f"расположите {config.SHIP_SIZES[self.__number_ships]}" + "-х" * (
                config.SHIP_SIZES[self.__number_ships] != 1) + " палубный корабль"
        self.__lbl = tk.Label(self.__window,
                              font=("AA Duke-Fill", 10, "bold"),
                              text=self.__text_before_timer,
                              justify="center",
                              borderwidth=1,
                              relief="solid")
        self.__lbl.pack(fill="both", anchor="s")
        canvas.pack(anchor="w")
        self.__starting_time = time()
        self.__window.after_idle(self.__loop, 0)  # start endless __loop
        self.__window.mainloop()

    def __update_ships(self):
        if len(config.SHIP_SIZES) > self.__number_ships and len(self.__ship) == config.SHIP_SIZES[self.__number_ships]:
            if not self.__check_correct_ship():
                for x, y in self.__ship:
                    self.__buttons[y][x].config(command=lambda a=x, b=y: self.__add(a, b),
                                                bg="aqua",
                                                activebackground='snow',
                                                state="normal")
                self.__ship = []
                messagebox.showinfo(title="Ошибка ввода",
                                    message="Отмеченные клетки не являются необходимым кораблём. Попытайтесь снова.")
            else:
                self.__number_ships += 1
                if len(config.SHIP_SIZES) == self.__number_ships:
                    for i in range(config.ROW):
                        for j in range(config.COLUMN):
                            self.__buttons[i][j]["state"] = "disabled"
                    self.__lbl["text"] = "Ожидайте соперника"
                    self.__is_ready = True
                else:
                    self.__text_before_timer = f"расположите {config.SHIP_SIZES[self.__number_ships]}" + "-х" * (
                            config.SHIP_SIZES[self.__number_ships] != 1) + " палубный корабль"
                    self.__lbl["text"] = self.__text_before_timer
                    if self.__presence_timer:
                        self.__lbl["text"] += f"({str(self.__timer)})"
                real_ship = Ship(self.__ship)
                for x, y in self.__ship:
                    self.__real_field[y][x] = real_ship
                for x, y in real_ship.get_environment():
                    self.__buttons[y][x].config(command=0,
                                                bg="powder blue",
                                                activebackground="powder blue",
                                                state="disabled")
                self.__ship = []

    def __check_correct_ship(self):
        if len(self.__ship) == 1:
            return True
        self.__ship.sort()
        editing_coord = []
        for i in range(len(self.__ship) - 1):
            editing_coord.append((self.__ship[i + 1][0] - self.__ship[i][0],
                                  self.__ship[i + 1][1] - self.__ship[i][1]))
        for i in range(len(editing_coord) - 1):
            if editing_coord[i + 1] != editing_coord[i] or \
                    ((0, 1) != editing_coord[i] and (1, 0) != editing_coord[i]):
                return False
        if (0, 1) != editing_coord[-1] and (1, 0) != editing_coord[-1]:
            return False
        return True

    def __update_timer(self):
        if time() - self.__starting_time >= config.TIME_WAITING_CONSTRUCTOR_FIELD - self.__timer + 1:
            self.__timer = max(config.TIME_WAITING_CONSTRUCTOR_FIELD - int(time() - self.__starting_time), 0)
            self.__lbl["text"] = self.__text_before_timer + f"({str(self.__timer)})"
            if self.__timer == 0 and not self.__window.is_destroyed():
                self.__real_field = []
                self.__is_ready = True
                if messagebox.showerror(title="Ты чего наделал!?", message="Время вышло, вы проиграли :("):
                    self.__window.destroy()

    def __loop(self, n):
        if self.__window.is_destroyed():
            self.__real_field = []
            self.__is_ready = True
            return
        if self.__presence_timer:
            self.__update_timer()
        if not self.__is_ready:
            self.__update_ships()
            self.__window.after(1, self.__loop, n + 1)  # endless __loop with delay
        else:
            self.__window.destroy()

    def get(self):
        if not self.__is_need_for_randomness:
            self.__window.destroy()
        if self.__is_ready:
            return self.__real_field
        return False


class AutomaticArrangements:
    __real_field = [["zeros and Ships"]]
    __probability_field = [(int, int)]
    __dict_index_elem = {(int, int): int}

    def __init__(self):
        check = False
        while not check:
            check = self.__attempt_to_arrange_the_ships()

    def get_field(self):
        return self.__real_field

    def __attempt_to_arrange_the_ships(self):
        # runs into the depth of recursion for non-standard field
        self.__probability_field = [(x, y) for x in range(config.COLUMN) for y in range(config.ROW)]
        self.__dict_index_elem = {(x, y): x * config.ROW + y for x in range(config.COLUMN) for y in range(config.ROW)}
        self.__real_field = [[0 for _ in range(config.COLUMN)] for _ in range(config.ROW)]
        return self.__arrange_the_ships()

    def __arrange_the_ships(self):
        number_ships = 0
        while number_ships != len(config.SHIP_SIZES):
            if len(self.__probability_field) - 1 < 0:
                return False
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
                    self.__real_field[y][x] = real_ship

                for x, y in real_ship.get_environment():
                    index = self.__dict_index_elem[(x, y)]
                    # -2 means that the unsuitable cells from environment ships
                    self.__remove_cell(index, -2)
        return True

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
