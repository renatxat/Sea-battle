import tkinter as tk
from random import randint

from application_game_with_bot import Application
from client import Client
from wrappers import Window
from wrappers import Button


class Menu:
    __window = ["tk.Tk()"]

    def __init__(self):
        self.__window = Window()
        button1 = Button(self.__window,
                         text="Играть с ботом",
                         font=("Trebuchet MS", 13, "bold"),
                         command=lambda: self.__create_select_first_move_window())
        button1.pack(anchor="center", expand=1, fill="both", ipadx=10, ipady=10)

        button2 = Button(self.__window,
                         text="Играть по сети",
                         font=("Trebuchet MS", 13, "bold"),
                         command=lambda: self.__create_select_type_of_generation_field_window(is_game_bot=False))
        button2.pack(anchor="center", expand=1, fill="both", ipadx=10, ipady=10)

        self.__window.mainloop()

    def __create_select_first_move_window(self):
        self.__window.destroy()
        self.__window = Window(False)
        button1 = Button(self.__window,
                         text="Безумно можно быть первым",
                         font=("Trebuchet MS", 13, "bold"),
                         command=lambda: self.__create_select_type_of_generation_field_window(
                             is_game_bot=True,
                             is_my_first_move=True))
        button1.pack(anchor="center", expand=1, fill="both", ipadx=10, ipady=10)

        button2 = Button(self.__window,
                         text="Пусть начинает бот",
                         font=("Trebuchet MS", 13, "bold"),
                         command=lambda: self.__create_select_type_of_generation_field_window(
                             is_game_bot=True,
                             is_my_first_move=False))
        button2.pack(anchor="center", expand=1, fill="both", ipadx=10, ipady=10)

        button3 = Button(self.__window,
                         text="Пусть решит рандом",
                         font=("Trebuchet MS", 13, "bold"),
                         command=lambda: self.__create_select_type_of_generation_field_window(
                             is_game_bot=True))
        button3.pack(anchor="center", expand=1, fill="both", ipadx=10, ipady=10)

        button4 = Button(self.__window,
                         text="Назад",
                         font=("Trebuchet MS", 13, "bold"),
                         command=lambda: [self.__window.destroy(), self.__init__()])
        button4.pack(anchor="center", expand=1, fill="both", ipadx=10, ipady=10)

    def __create_select_type_of_generation_field_window(self, is_game_bot, is_my_first_move=bool(randint(0, 1))):
        self.__window.destroy()
        self.__window = Window(False)
        button1 = Button(self.__window,
                         text="Расставить корабли самостоятельно",
                         font=("Trebuchet MS", 13, "bold"),
                         command=lambda: self.__start_game(is_game_bot, is_my_first_move, False))
        button1.pack(anchor="center", expand=1, fill="both", ipadx=10, ipady=10)

        button2 = Button(self.__window,
                         text="Расставить корабли автоматически",
                         font=("Trebuchet MS", 13, "bold"),
                         command=lambda: self.__start_game(is_game_bot, is_my_first_move, True))
        button2.pack(anchor="center", expand=1, fill="both", ipadx=10, ipady=10)

        button3 = Button(self.__window,
                         text="Назад",
                         font=("Trebuchet MS", 13, "bold"),
                         command=lambda: [self.__window.destroy(),
                                          self.__create_select_first_move_window()] if is_game_bot else [
                             self.__window.destroy(), self.__init__()])
        button3.pack(anchor="center", expand=1, fill="both", ipadx=10, ipady=10)

    def __start_game(self, is_game_bot, is_my_first_move, is_need_for_randomness):
        self.__window.destroy()
        if is_game_bot:
            Application(is_need_for_randomness, is_my_first_move)
        else:
            Client(is_need_for_randomness)


if __name__ == "__main__":
    Menu()
