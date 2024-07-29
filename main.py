import tkinter as tk
from random import randint

from application_game_with_bot import Application
from client import Client
from window import Window


class Menu:
    __window = ["tk.Tk()"]

    def __init__(self):
        self.__window = Window()
        button1 = tk.Button(self.__window,
                            text="Играть с ботом",
                            font=("Comic Sans MS", 13, "bold"),
                            command=self.__create_select_first_move_window)
        button1.pack(anchor="center", expand=1, fill="both")

        button2 = tk.Button(self.__window,
                            text="Играть по сети",
                            font=("Comic Sans MS", 13, "bold"),
                            command=lambda: self.__start_game(False))
        button2.pack(anchor="center", expand=1, fill="both")

        self.__window.mainloop()

    def __create_select_first_move_window(self):
        self.__window.destroy()
        self.__window = Window(False)
        button1 = tk.Button(self.__window,
                            text="Безумно можно быть первым",
                            font=("Comic Sans MS", 13, "bold"),
                            command=lambda: self.__start_game(True, True))
        button1.pack(anchor="center", expand=1, fill="both")

        button2 = tk.Button(self.__window,
                            text="Пусть начинает бот",
                            font=("Comic Sans MS", 13, "bold"),
                            command=lambda: self.__start_game(True, False))
        button2.pack(anchor="center", expand=1, fill="both")

        button3 = tk.Button(self.__window,
                            text="Пусть решит рандом",
                            font=("Comic Sans MS", 13, "bold"),
                            command=lambda: self.__start_game(True))
        button3.pack(anchor="center", expand=1, fill="both")

    def __start_game(self, is_game_bot, is_my_first_move=bool(randint(0, 1))):
        self.__window.destroy()
        if is_game_bot:
            Application(is_my_first_move)
        else:
            Client()


Menu()
