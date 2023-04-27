from ship import Ship
from application_game import Application
import config

import tkinter as tk
from tkinter import messagebox
from random import randint


class ConstructorFields:
    __lbl = ["tk.label"]
    __buttons = []
    __ship = [(int, int)]
    __number_ships = 0
    __window = ["tk.Tk()"]
    __real_field = ["zeros and Ships"]
    __is_my_first_move = True
    __is_game_bot = True

    def __init__(self):
        self.__real_field = [[0 for _ in range(config.column)] for _ in range(config.row)]
        self.__ship = []
        self.__window = tk.Tk()
        button1 = tk.Button(self.__window,
                            text="Играть с ботом",
                            font=("Comic Sans MS", 13, "bold"),
                            command=self.create_select_first_move_window)
        button1.pack(anchor="center", expand=1, fill="both")

        button2 = tk.Button(self.__window,
                            text="Играть по сети",
                            font=("Comic Sans MS", 13, "bold"),
                            command=lambda: self.create_creation_window(False))
        button2.pack(anchor="center", expand=1, fill="both")

        self.tune_window()
        self.__window.mainloop()

    def tune_window(self):
        self.__window.resizable(width=False, height=False)
        self.__window.title("Морской Бой")
        self.__window.tk.call("wm", "iconphoto", self.__window._w, tk.PhotoImage(file="main_icon.png"))
        self.__window.protocol("WM_DELETE_self.window", self.__on_closing)
        x = (self.__window.winfo_screenwidth() -
             self.__window.winfo_reqwidth()) / 2
        y = (self.__window.winfo_screenheight() -
             self.__window.winfo_reqheight()) / 2
        self.__window.wm_geometry("+%d+%d" % (x, y))

    def create_select_first_move_window(self):
        self.__window.destroy()
        self.__window = tk.Tk()
        self.tune_window()
        button1 = tk.Button(self.__window,
                            text="Безумно можно быть первым",
                            font=("Comic Sans MS", 13, "bold"),
                            command=lambda: self.create_creation_window(True, True))
        button1.pack(anchor="center", expand=1, fill="both")

        button2 = tk.Button(self.__window,
                            text="Пусть начинает бот",
                            font=("Comic Sans MS", 13, "bold"),
                            command=lambda: self.create_creation_window(True, False))
        button2.pack(anchor="center", expand=1, fill="both")

        button3 = tk.Button(self.__window,
                            text="Пусть решит рандом",
                            font=("Comic Sans MS", 13, "bold"),
                            command=lambda: self.create_creation_window(True))
        button3.pack(anchor="center", expand=1, fill="both")

    def create_creation_window(self, is_game_bot, is_my_first_move=bool(randint(0, 1))):
        self.__is_game_bot = is_game_bot
        self.__is_my_first_move = is_my_first_move
        if not self.__is_game_bot:
            messagebox.showinfo(title="Могли, но не стали",
                                message="Данный режим не доступен в вашей стране.")
            return
        self.__window.destroy()
        self.__window = tk.Tk()
        self.tune_window()
        canvas = tk.Canvas(self.__window,
                           width=config.column * config.size_of_cell - 2,
                           height=config.row * config.size_of_cell - 2)
        for i in range(config.row):
            temp = []
            for j in range(config.column):
                btn = tk.Button(canvas,
                                bg="aqua",
                                width=config.size_of_cell,
                                height=config.size_of_cell,
                                borderwidth=2)
                temp.append(btn)
            self.__buttons.append(temp)
        for i in range(config.row):
            for j in range(config.column):
                self.__buttons[i][j]["command"] = lambda x=j, y=i: self.add(x, y)
        for i in range(config.row):
            for j in range(config.column):
                self.__buttons[i][j].pack(expand=False, side="top")
                canvas.create_window((j * config.size_of_cell, i * config.size_of_cell),
                                     anchor="nw",
                                     window=self.__buttons[i][j])
        self.__lbl = tk.Label(self.__window,
                              font=("Comic Sans MS", 11, "bold"),
                              text=f"расположите 4-х палубный корабль",
                              justify="center",
                              borderwidth=1,
                              relief="solid")
        self.__lbl.pack(fill="both", anchor="s")
        canvas.pack(anchor="w")
        self.__window.after_idle(self.loop, 0)  # start endless __loop

    def __on_closing(self):
        if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
            self.__window.destroy()

    def add(self, x, y):
        self.__ship.append((x, y))
        self.__buttons[y][x].config(command=0,
                                    bg="slateblue",
                                    state="disabled")

    def update_ships(self):
        if len(config.ship_sizes) == self.__number_ships:
            self.__window.destroy()
            window = tk.Tk()
            Application(window, self.__real_field, self.__is_my_first_move, self.__is_game_bot)
        elif len(self.__ship) == config.ship_sizes[self.__number_ships]:
            if not self.check_correct_ship():
                for x, y in self.__ship:
                    self.__buttons[y][x].config(command=lambda a=x, b=y: self.add(a, b),
                                                bg="aqua",
                                                state="normal")
                self.__ship = []
                messagebox.showinfo(title="Ошибка ввода",
                                    message="Отмеченные клетки не являются необходимым кораблём. Попытайтесь снова.")
            else:
                self.__number_ships += 1
                if len(config.ship_sizes) == self.__number_ships:
                    self.__lbl["text"] = "генерируем поле"
                else:
                    self.__lbl["text"] = f"расположите {config.ship_sizes[self.__number_ships]}" + "-х" * (
                            config.ship_sizes[self.__number_ships] != 1) + " палубный корабль"
                real_ship = Ship(self.__ship)
                for x, y in self.__ship:
                    self.__real_field[y][x] = real_ship
                for x, y in real_ship.get_environment():
                    self.__buttons[y][x].config(command=0,
                                                bg="powderblue",
                                                state="disabled")
                self.__ship = []

    def check_correct_ship(self):
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

    def loop(self, n):
        self.update_ships()
        self.__window.after(1, self.loop, n + 1)  # endless __loop with delay


ConstructorFields()
